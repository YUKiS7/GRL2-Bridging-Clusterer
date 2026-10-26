# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A thesis data-analysis project built around Jupyter notebooks in `notebooks/`. There is no package, build step, linter or test suite. The notebooks are numbered in pipeline order:
- `00_what-am-i-doing.ipynb`: the original scratch/lab notebook, kept as a record of how the work got here. Its paths still assume the repo root, so it no longer runs as is.
- `01_preprocessing.ipynb`: loads the raw JSON, builds features and exports them as CSV. No plotting.
- `02_data-analysis.ipynb`: loads the exported CSVs for plots and clustering (not started yet).

## Environment

All Python runs inside a Docker container (Python 3.12.4, JupyterLab, pandas, numpy, matplotlib, scikit-learn). See `jupyter_docker/Dockerfile`. To add a library, add it to the Dockerfile's `pip3 install` list and rebuild.

```sh
docker compose up --build        # JupyterLab at http://localhost:8888 (no token/password)
```

The repo root is mounted at `/home` in the container. Notebooks live in `notebooks/`, and a kernel runs in its notebook's folder, so notebook paths are relative to `notebooks/` (e.g. `../data/...`).

Run the notebook headlessly inside the container:

```sh
docker exec -i grl2-jupyter-1 jupyter nbconvert --to notebook --execute notebooks/01_preprocessing.ipynb --stdout > /dev/null
```

## Git: notebook output stripping

`.gitattributes` sends `*.ipynb` through a `strip-notebook-output` filter. That filter is defined in `.sharedgitconfig`, and it runs `nbconvert` **inside the running container `grl2-jupyter-1`**. Two consequences:
- The container must be running for `git add`, `git diff` and `git commit` to work on notebooks.
- The filter must be registered through a git `include.path` pointing at `.sharedgitconfig`. To check it, run `git config --get filter.strip-notebook-output.clean`.

## Data

`data/` and `files/` are gitignored and exist only locally.
- `data/thesis_data_*.json` is a list of session records. Each record has top-level fields (for example `fastBuilderMode` and `idAnonymous`) and a nested, variable-length `stepData` list.
- `data/notebooks_exports/` holds the CSVs written by `01_preprocessing` (see below).
- `files/` holds the thesis proposal (`Thesis_Proposal.pdf`) and `stakeholder_meetings.txt`, which give the project context. It also holds the stakeholder mcplayhd's material: `mcplayhd_concept_java.txt` (the Java plugin draft that section 03 of `01_preprocessing` ports) and `mcplayhd_concept_notebook.ipynb` (their own clustering experiments).

## Notebook pipeline (current state)

`01_preprocessing.ipynb` keeps all imports in one cell and all constants in a settings cell (`UPPER_CASE`). The logic is split into small helper functions, and each loop collects one dict per row into a DataFrame. Each section starts from the raw `data` independently:

1. **Per-replay features** → `speed_to_block_per_click.csv`, one row per replay.
   - `movement_per_tick(steps)`: distance moved between consecutive steps (length N-1).
   - `longest_active_window(movement)`: a `slice` of the longest stretch with no idling (movement < `IDLE_THRESHOLD` for more than `MAX_IDLE_TICKS` ticks in a row), or `None` if it is shorter than `MIN_WINDOW_SIZE`.
   - `replay_features(item)`: within that window, computes `blocks_per_click` (total blocks / total clicks) and `avg_speed` (blocks per second) and adds `window_share`. It drops replays with fewer than `MIN_BLOCKS` blocks or zero clicks. Clicks and blocks use `steps[1:]` so they align with `movement`.
2. **Random windows for the neural network** → `wide_table.csv`, one row per replay and 361 columns.
   - `random_window(steps)`: `RANDOM_WINDOW_SIZE` consecutive steps taken from inside the longest active window, or `None`.
   - `window_features(item, window)`: produces the columns `idAnonymous`, `fastBuilderMode`, `pingAvg` and `pingJitter`, then `movement_*`, `yawChange_*` and `pitchChange_*` (the change features start at `_1`, with yaw wrapped to -180..180), then `clicks_*`, `sneaking_*` and `blocksChanged_*` (from `_0`).
   - `random.seed(RANDOM_SEED)` is called at the top of the loop cell, so the export is reproducible.
3. **McPlayHD concept (work in progress)**: a port of `files/mcplayhd_concept_java.txt`, one row per replay. The loop and export cells are still TODO placeholders, and a `# temp cell` for testing sits after the helpers. Its constants are `CONCEPT_WINDOW_SIZE`, `Y_WEIGHT`, `MAX_CLICKS` and `EYE_HEIGHT`.
   - `last_block_tick(steps)`: the index of the last step that placed a non-`AIR` block, or `None`.
   - `best_window_start(steps, last_tick)`: the start of the `CONCEPT_WINDOW_SIZE` window that ends before `last_tick`, doesn't end lower than it starts, and covers the largest squared distance from start to end (Y weighted by `Y_WEIGHT`). Returns `None` if no window fits. Java falls back to 0 instead.
   - `blocks_before(steps, start)`: a set of `(x, y, z)` tuples of non-`AIR` blocks placed before the window.
   - `concept_window_features(item, start, already_placed)`: the columns `idAnonymous` and `fastBuilderMode`, then `dx_*`, `dy_*`, `dz_*`, `yaw_change_*` and `pitch_change_*` (from `_1`, yaw wrapped), then `sneaking_*` and `clicks_*` (from `_0`, clicks capped at `MAX_CLICKS`). There's no zero-padding, because every window is full length. Still to do: per-tick `newBlock_*`, plus `blockDx/Dy/Dz_*`, the first new block's offset from the player's eyes (`y + EYE_HEIGHT`). New blocks are also added to `already_placed`, as in Java.
   - The plan is one DataFrame/CSV with the `fastBuilderMode` column. The per-mode split for clustering happens in `02_data-analysis`.

Known data quirks: ping is rarely updated, so `pingJitter` is mostly 0. About 10% of steps have more blocks than clicks, and a few replays have `blocks_per_click` > 1.

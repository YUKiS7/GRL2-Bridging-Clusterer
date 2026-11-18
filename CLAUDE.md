# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A thesis data-analysis project built around Jupyter notebooks in `notebooks/`. There is no package, build step, linter or test suite. The notebooks are numbered in pipeline order:
- `00_what-am-i-doing.ipynb`: the original scratch/lab notebook, kept as a record of how the work got here. Its paths still assume the repo root, so it no longer runs as is.
- `01_sampling.ipynb`: draws a balanced sample (`SAMPLE_PER_MODE` replays per mode) from the bulk data in `data/bulk/` and writes it to `data/sampled_replays.jsonl` (70000 replays, one JSON per line, ~7.3 GB). It does two passes over the files (index, then write) and uses `RANDOM_SEED = 18`. Read the jsonl line by line, never all at once.
- `02_preprocessing.ipynb`: streams `data/sampled_replays.jsonl`, builds features and exports them as CSV. No plotting.
- `03_data-analysis.ipynb`: loads the exported CSVs, runs per-mode clustering and exports replay IDs to look up in Minecraft.
- `04_cluster_labeling.ipynb`: joins the hand-made `data/replay_labels.csv` (`idAnonymous, fastBuilderMode, playstyle, suspicious, notes`) onto each `labeling_cluster_export_<method>.csv` and votes per cluster. Since 2026-11-17 (mcplayhd asked for no fancy logic), `vote_cluster(df_cluster_voters)` gets one cluster's non-outlier voters and returns `technique_votes` (str of `{part: share of voters}`, `ac` filtered out but ac voters still in the denominator) and `suspicious_votes` (str of `{0-3: count}`, ac voters left out). There is no `label`/`too_small` anymore; clusters without voters get `{}`. The old readable-label logic is kept at the bottom as `vote_cluster_fancy` and is NOT the current output. mcplayhd doesn't care about ac itself; the question is only whether clusters exist because of clicks. `label_replays` then gives every replay its cluster's votes plus `confidence = 1 - percentile rank of distance within its cluster`. One execute cell per method writes `cluster_labels_<method>.csv` (one row per cluster) and `labeled_replays_<method>.csv` (one row per replay). A browse cell at the end shows one cluster's voters and its vote.
- `05_knn.ipynb`: classifies a new dataset of 10000 replays (`NEW_DATA_PATH`) with k-NN per method and mode. Since 2026-11-17 it predicts the `cluster` (trained on the joblib `labels`) and then merges that cluster's votes from `cluster_labels_<method>.csv`. It holds verbatim copies of the 02 helpers and settings, which must be re-copied whenever 02 changes, then fits `KNeighborsClassifier` on the joblib positions (`scaled` / `reduced`) with the cluster ids, and transforms new replays with the saved scaler (and pca) of their mode.

## Environment

All Python runs inside a Docker container (Python 3.12.4, JupyterLab, pandas, numpy, matplotlib, scikit-learn). See `jupyter_docker/Dockerfile`. To add a library, add it to the Dockerfile's `pip3 install` list and rebuild.

```sh
docker compose up --build        # JupyterLab at http://localhost:8888 (no token/password)
```

The repo root is mounted at `/home` in the container. Notebooks live in `notebooks/`, and a kernel runs in its notebook's folder, so notebook paths are relative to `notebooks/` (e.g. `../data/...`).

Run the notebook headlessly inside the container:

```sh
docker exec -i grl2-jupyter-1 jupyter nbconvert --to notebook --execute notebooks/02_preprocessing.ipynb --stdout > /dev/null
```

## Git: notebook output stripping

`.gitattributes` sends `*.ipynb` through a `strip-notebook-output` filter. That filter is defined in `.sharedgitconfig`, and it runs `nbconvert` **inside the running container `grl2-jupyter-1`**. Two consequences:
- The container must be running for `git add`, `git diff` and `git commit` to work on notebooks.
- The filter must be registered through a git `include.path` pointing at `.sharedgitconfig`. To check it, run `git config --get filter.strip-notebook-output.clean`.

## Data

`data/` and `files/` are gitignored and exist only locally.
- `data/thesis_data_*.json` is a list of session records. Each record has top-level fields (for example `fastBuilderMode` and `idAnonymous`) and a nested, variable-length `stepData` list.
- `data/bulk/` holds the bulk data from mcplayhd: 50 JSON files (~26 GB) with 10000 replays each, 500000 in total. `idAnonymous` is unique across all files (1..500000). The first file is the old single dataset. The files are too big to load at once inside the container (15.6 GB RAM limit), so code has to go through them one file at a time.
- `data/notebooks_exports/` holds the CSVs written by `02_preprocessing`, plus from `03_data-analysis` per method (`movement_camera`, `mcplayhd_concept`): the watch list `cluster_export_<method>.csv`, the full assignment `labeling_cluster_export_<method>.csv` (`idAnonymous, mode, cluster, distance, is_outlier`, one row per replay) and `cluster_models_<method>.joblib` (the whole results dict per mode: ids, positions `scaled`/`reduced`, scaler, pca, kmeans, labels, nearest_distances, is_outlier; load with `joblib.load`, same scikit-learn version). `04_cluster_labeling` adds `cluster_labels_<method>.csv` and `labeled_replays_<method>.csv`.
- `data/validation.zip` holds the new data for `05_knn`: one json list (`thesis_data_1794427250445.json`, ~590 MB unpacked) with 10000 replays, ids 500001..510000 (no overlap with the bulk), modes not balanced (EXTRASHORT 5349 … INCLINED 357). It has an extra field `minecraftProtocolVersion`. 05 reads it straight from the zip.
- `data/replay_labels.csv` holds the 1170 hand labels (`playstyle` parts joined by `_`, `suspicious` 0–3).
- `files/` holds the thesis proposal (`Thesis_Proposal.pdf`) and `stakeholder_meetings.txt`, which give the project context. It also holds the stakeholder mcplayhd's material: `mcplayhd_concept_java.txt` (the Java plugin draft that section 03 of `02_preprocessing` ports) and `mcplayhd_concept_notebook.ipynb` (their own clustering experiments).

## Notebook pipeline (current state)

All computed columns are snake_case. Only `idAnonymous` and `fastBuilderMode` keep their raw JSON names.

`02_preprocessing.ipynb` keeps all imports in one cell and all constants in a settings cell (`UPPER_CASE`). The logic is split into small helper functions, and each loop collects one dict per row into a DataFrame. The input is `INPUT_DATA` (the sample jsonl), read through the generator `iter_data()`, which yields one replay at a time. Each section loops over `iter_data()` on its own (one pass takes several minutes) and prints `dataframe holds X out of 70000 replays` as a sanity check:

1. **Per-replay features** → `speed_to_block_per_click.csv`, one row per replay (69084 rows).
   - `movement_per_tick(steps)`: distance moved between consecutive steps (length N-1).
   - `longest_active_window(movement)`: a `slice` of the longest stretch with no idling (movement < `IDLE_THRESHOLD` for more than `MAX_IDLE_TICKS` ticks in a row), or `None` if it is shorter than `MIN_WINDOW_SIZE`.
   - `replay_features(item)`: within that window, computes `blocks_per_click` (total blocks / total clicks) and `avg_speed` (blocks per second) and adds `window_share`. It drops replays with fewer than `MIN_BLOCKS` blocks or zero clicks. Clicks and blocks use `steps[1:]` so they align with `movement`.
2. **Random windows for the neural network** → `wide_table.csv`, one row per replay and 361 columns (69301 rows).
   - `random_window(steps)`: `RANDOM_WINDOW_SIZE` consecutive steps taken from inside the longest active window, or `None`.
   - `window_features(item, window)`: produces the columns `idAnonymous`, `fastBuilderMode`, `ping_avg` and `ping_jitter`, then `movement_*`, `yaw_change_*` and `pitch_change_*` (the change features start at `_1`, with yaw wrapped to -180..180), then `clicks_*`, `sneaking_*` and `blocks_changed_*` (from `_0`).
   - `random.seed(RANDOM_SEED)` is called at the top of the loop cell, so the export is reproducible.
3. **McPlayHD concept** → `mcplayhd_concept.csv`, a port of `files/mcplayhd_concept_java.txt` with one row per replay (69005 rows, 547 columns). The loop skips a replay when `best_window_start` or `concept_window_features` returns `None`. Its constants are `CONCEPT_WINDOW_SIZE`, `Y_WEIGHT`, `MAX_CLICKS` and `EYE_HEIGHT`.
   - `last_block_tick(steps)`: the index of the last step that placed a non-`AIR` block, or `None`.
   - `best_window_start(steps, last_tick)`: the start of the `CONCEPT_WINDOW_SIZE` window that ends before `last_tick`, doesn't end lower than it starts, and covers the largest squared distance from start to end (Y weighted by `Y_WEIGHT`). Returns `None` if no window fits. Java falls back to 0 instead.
   - `blocks_before(steps, start)`: a set of `(x, y, z)` tuples of non-`AIR` blocks placed before the window.
   - `concept_window_features(item, start, already_placed)`: the columns `idAnonymous` and `fastBuilderMode`, then `dx_*`, `dy_*`, `dz_*`, `yaw_change_*` and `pitch_change_*` (from `_1`, yaw wrapped), then `sneaking_*` and `clicks_*` (from `_0`, clicks capped at `MAX_CLICKS`). After those come per tick (from `_0`) `new_block_*` (1 if the tick placed a block not in `already_placed`) and `block_dx/dy/dz_*`, the first new block's offset from the player's eyes (`y + EYE_HEIGHT`), or 0 if there is no new block. New blocks are added to `already_placed`, as in Java. There's no zero-padding, because every window is full length. It returns `None` if the window has no new block at all. That's a deliberate filter: new replays for a later nearest-neighbour lookup must go through the same helpers, and `None` means "not classifiable".
   - The plan is one DataFrame/CSV with the `fastBuilderMode` column. The per-mode split for clustering happens in `03_data-analysis`.

Known data quirks: ping is rarely updated, so `ping_jitter` is mostly 0. About 10% of steps have more blocks than clicks, and a few replays (0–6 per mode) have `blocks_per_click` > 1. `blocks_per_click` has a dense line at exactly 1.0, plus stripes at simple ratios (0.5, 0.33, 0.25) that come from small click counts.

`03_data-analysis.ipynb` follows the same style (one imports cell, one settings cell, `RANDOM_SEED = 42`). The sections are meant to be self-contained, and the user wants to keep the older single-mode sections 03/04 next to their all-modes versions 03b/04b.
- **helpers** (right after settings): `cluster_export_rows(method, results)` is the one shared helper. `results` is a dict mode → result dict, and the function only reads four keys from each result: `ids`, `labels`, `nearest_distances` and `is_outlier`. So any clustering method that fills those keys can be exported (for HDBSCAN: `is_outlier = labels == -1`, distance to the nearest medoid; label `-1` is skipped as a cluster). Per cluster it takes the non-outlier members sorted by distance and picks the ones at `EXPORT_EXAMPLE_PERCENTILES` (0% = `center`, the rest are `example`, duplicates in tiny clusters are skipped). Per mode it adds the `EXPORT_OUTLIER_COUNT` farthest outliers (`outlier`). It returns a long DataFrame with the columns `method, mode, cluster, cluster_size, role, rank, distance, idAnonymous, notes`.
- **01 / 02**: movement and camera-turn summaries (mean/std) per mode.
- **03 / 03b, movement & camera**: features `movement_avg`, `movement_std` and `turn_avg_log` (log1p of the mean camera turn per tick) → StandardScaler → k-means per mode with `CLUSTER_COUNTS`, outliers = top `CLUSTER_OUTLIER_PERCENTILE` by distance to the nearest centre. Results are in `clustering_results[mode]`. 03b ends with an `export` subsection writing `cluster_export_movement_camera.csv` (`method = "movement_camera"`). Some modes have micro clusters of 1–7 far-out replays; the user accepts them.
- **04 / 04b, mcplayhd concept**: StandardScaler → PCA(0.95) → k-means per mode with `MCPLAYHD_CLUSTER_COUNTS`, results in `mcplayhd_results[mode]`. The 03b and 04b export cells each write the watch list, the full assignment and the joblib models file (see Data).
- **05 / 05b, blocks per click**: k-means (05) and an HDBSCAN test (05b) on `blocks_per_click` and `avg_speed`. Both give arbitrary clusters, so the approach is dropped for clustering. The useful signal is a rule: replays with `blocks_per_click` ≥ ~0.95 and high speed (> ~6 b/s) look like auto-place cheats when checked in game.

Results dicts are filled section by section, and plain names like `labels` or `modes_list` get reused across sections. When code in one section reads a variable from another, give it a section-specific name (e.g. `hdbscan_labels`) so re-running an earlier section can't overwrite it.

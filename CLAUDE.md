# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A thesis data-analysis project built around one Jupyter notebook, `what-am-i-doing.ipynb`. There is no package, build step, linter or test suite. The work so far loads the gameplay telemetry dataset and prepares fixed-size windows for a neural network.

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
- `files/` holds the thesis proposal (`Thesis_Proposal.pdf`) and `stakeholder_meetings.txt`, which give the project context.

## Notebook pipeline (current state)

1. Load the JSON. Then flatten it into a DataFrame by replacing `stepData` with a `numSteps` count. This is only for inspection.
2. Build training samples by taking a random fixed-length window (`WINDOW_SIZE = 60`) from each record's `stepData` and skipping records that are shorter. Each sample keeps `fastBuilderMode` (the apparent label) and `idAnonymous`.

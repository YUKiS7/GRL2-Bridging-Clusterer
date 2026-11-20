Put the model bundle here (too big for git):

- `model_bundle.joblib`: everything that belongs to one model, written by the "model bundle" cell at the end of `04_cluster_labeling` (there called `model_bundle_<version>.joblib`). It holds:
  - `model_version`: e.g. `v3_noclicks`, sent with every response
  - `feature_settings`: the window settings the features were built with (`CONCEPT_WINDOW_SIZE`, `Y_WEIGHT`, `MAX_CLICKS`, `EYE_HEIGHT`)
  - `modes`: per mode the scaler, pca, training points and the cluster of each point
  - `cluster_votes`: per cluster the technique shares and suspicious counts from the hand-label voting
  - `knn_neighbours`: k of the k-NN that puts new replays into a cluster

Nothing model-specific lives in the code, so swapping the model means swapping this one file:

1. Run `04_cluster_labeling` (with the 04b execute cell before the bundle cell).
2. Copy `data/notebooks_exports/model_bundle_<version>.joblib` here as `model_bundle.joblib`.
3. Restart the server. The model is loaded on the first request and then kept in memory, so a running server keeps the old one until it restarts.

The bundle must be loaded with the same scikit-learn version it was saved with (see `requirements.txt`).

The current version is `v3_noclicks`.

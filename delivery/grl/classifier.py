"""new replays -> (cluster, confidence)"""
import pandas as pd

from grl.features import replay_to_row
from grl.model_store import get_knn, get_clustering_model, get_feature_settings


def cluster_id(mode, cluster):
    """global cluster id for the api, e.g. ("EXTRASHORT", 1) -> "EXTRASHORT_1" """
    return mode + "_" + str(cluster)


def to_model_space(mode_clustering_model, df_replays):
    """puts feature rows of one mode into the space the model was trained in (saved scaler, then pca), never refits

    mode_clustering_model: the clustering model of one mode (scaler, pca, positions, labels, ...)
    df_replays: dataframe of preprocessed replays from one mode
    returns scaled (and pca transformed) positions
    """
    df_features = df_replays[mode_clustering_model["scaler"].feature_names_in_]  # only the columns the scaler was trained on, in its order
    positions = mode_clustering_model["scaler"].transform(df_features)
    if "pca" in mode_clustering_model:
        positions = mode_clustering_model["pca"].transform(positions)
    return positions


def classify(replays):
    """list of replay dicts -> list of dicts {id, cluster, confidence}, cluster/confidence None if not classifiable

    keeps the input order, and every input id appears in the output
    """

    feature_settings = get_feature_settings()
    replay_rows = [replay_to_row(replay, feature_settings) for replay in replays]
    df_replays = pd.DataFrame([row for row in replay_rows if row is not None])

    predictions = {}

    if not df_replays.empty:
        for mode, df_mode in df_replays.groupby("fastBuilderMode"):
            if mode not in get_clustering_model():
                continue
            positions_transformed = to_model_space(get_clustering_model()[mode], df_mode)
            knn_model = get_knn(mode)

            predicted_clusters = knn_model.predict(positions_transformed)
            predicted_confidences = knn_model.predict_proba(positions_transformed).max(axis=1)

            for replay_id, cluster, confidence in zip(df_mode["idAnonymous"], predicted_clusters, predicted_confidences):
                predictions[replay_id] = {
                    "cluster": cluster_id(mode, cluster),
                    "confidence": confidence,
                }

    result = []
    for replay in replays:
        replay_id = replay["idAnonymous"]

        if replay_id in predictions:
            result.append({
                "id": replay_id,
                "cluster": predictions[replay_id]["cluster"],
                "confidence": predictions[replay_id]["confidence"],
            })
        else:
            result.append({
                "id": replay_id,
                "cluster": None,
                "confidence": None,
            })

    return result

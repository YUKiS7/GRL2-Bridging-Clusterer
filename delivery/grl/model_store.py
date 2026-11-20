"""loads the trained models lazily: only on the first call, then they stay in memory"""
from functools import lru_cache
from sklearn.neighbors import KNeighborsClassifier
import joblib

from grl.settings import (
    MODEL_BUNDLE_PATH,
)


@lru_cache
def get_model_bundle():
    """loads the bundle (written by 04) once: everything model-specific comes from here, so swapping the file swaps the model"""
    return joblib.load(MODEL_BUNDLE_PATH)


def get_clustering_model():
    """per mode: scaler, pca, training positions, cluster labels"""
    return get_model_bundle()["modes"]


def get_clusters_voted_labels():
    """list of dicts {mode, cluster, technique_votes, suspicious_votes}, votes as real dicts"""
    return get_model_bundle()["cluster_votes"]


def get_feature_settings():
    """the 02 settings the model was trained with, e.g. {"CONCEPT_WINDOW_SIZE": 50, "Y_WEIGHT": 0.5, ...}"""
    return get_model_bundle()["feature_settings"]


def get_model_version():
    """the version of the loaded model, e.g. "v3_noclicks" """
    return get_model_bundle()["model_version"]


@lru_cache
def get_knn(mode):
    """a fitted KNeighborsClassifier for one mode, fitted once on first use"""
    model = get_clustering_model()[mode]
    position_key = "reduced" if "pca" in model else "scaled"

    X_train = model[position_key] # the data used for the model -> basically all replays from training
    y_train = model["labels"] # the cluster each training replay got assigned -> 1 number per replay
    knn = KNeighborsClassifier(n_neighbors=get_model_bundle()["knn_neighbours"])
    return knn.fit(X_train, y_train)

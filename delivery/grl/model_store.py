"""loads the trained models lazily: only on the first call, then they stay in memory"""
from functools import lru_cache
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib

from grl.settings import CLUSTERING_MODEL_PATH, CLUSTERS_VOTED_LABELS_PATH, KNN_NEIGHBOURS, POSITION_KEY


@lru_cache
def get_clustering_model():
    """loads the model"""
    return joblib.load(CLUSTERING_MODEL_PATH)


@lru_cache
def get_knn(mode):
    """a fitted KNeighborsClassifier for one mode, fitted once on first use"""
    model = get_clustering_model()[mode]
    X_train = model[POSITION_KEY] # the data used for the model -> basically all replays from training
    y_train = model["labels"] # the cluster each training replay got assigned -> 1 number per replay
    knn = KNeighborsClassifier(n_neighbors=KNN_NEIGHBOURS)
    return knn.fit(X_train, y_train)


@lru_cache
def get_clusters_voted_labels():
    """clusters_voted_labels csv from 04 as a DataFrame, loaded once"""
    return pd.read_csv(CLUSTERS_VOTED_LABELS_PATH)

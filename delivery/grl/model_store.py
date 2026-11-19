"""loads the trained models lazily: only on the first call, then they stay in memory"""
from functools import lru_cache

from grl.settings import CLUSTERING_MODEL_PATH, CLUSTERS_VOTED_LABELS_PATH


@lru_cache
def get_cluster_models():
    """the results dict from 03 (mode -> scaler, pca, positions, labels, ...), loaded once"""
    # TODO: joblib.load
    pass


@lru_cache
def get_knn(mode):
    """a fitted KNeighborsClassifier for one mode, fitted once on first use"""
    # TODO: training data from get_cluster_models()[mode], fit, return
    pass


@lru_cache
def get_cluster_labels():
    """cluster_labels csv from 04 as a DataFrame, loaded once"""
    # TODO: pd.read_csv
    pass

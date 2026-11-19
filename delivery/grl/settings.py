"""all constants in one place (same values as in 02_preprocessing, must stay in sync with the trained models)"""
from pathlib import Path

# ---------- paths ----------
# delivery/models/, found relative to this file, so it works no matter where the server is started from
MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

MODEL_VERSION = "v3_noclicks"  # sent with every response
CLUSTERING_MODEL_PATH = MODELS_DIR / "clustering_model.joblib"
CLUSTERS_VOTED_LABELS_PATH = MODELS_DIR / "clusters_voted_labels.csv"

# ---------- mcplayhd concept ----------
CONCEPT_WINDOW_SIZE = 50 # window size in ticks for mcplayhd's approach
Y_WEIGHT = 0.5 # weight of the y distance when searching for the best window
MAX_CLICKS = 1 # clicks per tick get capped at this value
EYE_HEIGHT = 1.62 # height of the player's eyes above their position

# ---------- k-NN ----------
KNN_NEIGHBORS = 15
POSITION_KEY = "reduced"  # training positions in the joblib (after pca)

# ---------- labels ----------
# suspicious 0-3 from replay_labels.csv -> name in the api
SUSPICIOUS_LEVELS = {0: "legit", 1: "maybe", 2: "suspicious", 3: "blatant"}

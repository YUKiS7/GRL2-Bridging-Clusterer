"""server constants. everything that belongs to a model (version, feature settings, votes) is in the model bundle, not here"""
from pathlib import Path

# ---------- paths ----------
# delivery/models/, found relative to this file, so it works no matter where the server is started from
MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

API_VERSION = "1.0.0"  # version of the endpoints/schemas, raise it when they change (then regenerate the java client)
# one file with everything, swap it to swap the model: model_version, feature_settings, modes (per-mode models), cluster_votes (written by 04)
MODEL_BUNDLE_PATH = MODELS_DIR / "model_bundle.joblib"

# ---------- labels ----------
# suspicious 0-3 from replay_labels.csv -> name in the api
SUSPICIOUS_LEVELS = {0: "legit", 1: "maybe", 2: "suspicious", 3: "blatant"}

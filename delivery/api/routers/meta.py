"""GET /techniques, GET /suspicious_levels, GET /version"""
from fastapi import APIRouter

from api.schemas import TechniquesResponse, SuspiciousLevelsResponse, VersionResponse
from grl.clusters import technique_names
from grl.model_store import get_model_version
from grl.settings import SUSPICIOUS_LEVELS

router = APIRouter()

@router.get("/version", response_model=VersionResponse, operation_id="getVersion")
def get_version():
    return {
        "model_version": get_model_version(),
    }

@router.get("/techniques", response_model=TechniquesResponse, operation_id="getTechniques")
def get_techniques():
    return {
        "model_version": get_model_version(),
        "results": technique_names(),
    }

@router.get("/suspicious_levels", response_model=SuspiciousLevelsResponse, operation_id="getSuspiciousLevels")
def get_suspicious_levels():
    return {
        "model_version": get_model_version(),
        "results": list(SUSPICIOUS_LEVELS.values()),
    }

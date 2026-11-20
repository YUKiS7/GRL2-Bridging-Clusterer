"""GET /clusters"""
from fastapi import APIRouter

from api.schemas import ClustersResponse
from grl.clusters import describe_clusters
from grl.model_store import get_model_version

router = APIRouter()


@router.get("/clusters", response_model=ClustersResponse, operation_id="getClusters")
def get_clusters():
    return {
        "model_version": get_model_version(),
        "results": describe_clusters(),
    }

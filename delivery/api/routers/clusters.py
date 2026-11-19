"""GET /clusters"""
from fastapi import APIRouter

router = APIRouter()

# TODO: @router.get("/clusters", response_model=..., operation_id="getClusters")
# calls grl.clusters.describe_clusters

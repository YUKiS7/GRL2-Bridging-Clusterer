"""the fastapi app: only wires the routers together, no logic here

run locally: uvicorn api.main:app --reload   (from the delivery folder)
docs:        http://localhost:8000/docs
spec:        http://localhost:8000/openapi.json
"""
from fastapi import FastAPI

from api.routers import label, clusters, meta
from grl.settings import API_VERSION

app = FastAPI(
    title="GRL replay classifier",
    version=API_VERSION,  # api version, not the model version (that one is in every response)
    description=(
        "Classifies FastBuilder replays: POST /label returns a cluster label for each replay. "
        "GET /clusters describes every cluster with techniques and suspicion levels."
    ),
)

# the tag groups the endpoints in /docs and names the java class: "classifier" -> ClassifierApi
app.include_router(label.router, tags=["classifier"])
app.include_router(clusters.router, tags=["classifier"])
app.include_router(meta.router, tags=["classifier"])

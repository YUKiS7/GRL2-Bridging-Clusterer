"""the fastapi app: only wires the routers together, no logic here

run locally: uvicorn api.main:app --reload   (from the delivery folder)
docs:        http://localhost:8000/docs
spec:        http://localhost:8000/openapi.json
"""
from fastapi import FastAPI

from api.routers import label, clusters, meta

app = FastAPI(title="GRL replay classifier")  # TODO: version, description

app.include_router(label.router)
app.include_router(clusters.router)
app.include_router(meta.router)

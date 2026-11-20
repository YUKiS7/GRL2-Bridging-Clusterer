"""the json shapes of the api (pydantic models)

every class here becomes a class in the generated java client, so names matter.
Field(description=...) shows up in /docs and openapi.json, not in the responses.
"""
from pydantic import BaseModel, Field


# ---------- input ----------
class Location(BaseModel):
    x: float
    y: float
    z: float


class Position(BaseModel):
    x: float
    y: float
    z: float
    yaw: float
    pitch: float


class BlockChange(BaseModel):
    material: str
    loc: Location


class Step(BaseModel):
    playerPosition: Position
    sneaking: bool
    clicks: int
    blocksChanged: list[BlockChange]

class Replay(BaseModel):
    """one replay"""
    idAnonymous: int
    fastBuilderMode: str
    stepData: list[Step]


# ---------- POST /label ----------
class LabelResult(BaseModel):
    id: int
    cluster: str | None
    confidence: float | None


class LabelResponse(BaseModel):
    model_version: str
    results: list[LabelResult]


# ---------- GET /clusters ----------
class TechniqueShare(BaseModel):
    label: str
    share: float


class SuspiciousCount(BaseModel):
    level: str
    count: int


class ClusterDescription(BaseModel):
    id: str
    cluster_labels: list[TechniqueShare]
    suspicious_levels: list[SuspiciousCount]


class ClustersResponse(BaseModel):
    model_version: str
    results: list[ClusterDescription]


# ---------- GET /techniques ----------
class TechniquesResponse(BaseModel):
    model_version: str
    results: list[str]


# ---------- GET /suspicious_levels ----------
class SuspiciousLevelsResponse(BaseModel):
    model_version: str
    results: list[str]



# ---------- GET /version ----------
class VersionResponse(BaseModel):
    model_version: str

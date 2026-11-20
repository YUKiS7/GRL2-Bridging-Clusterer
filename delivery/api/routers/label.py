"""POST /label"""
from fastapi import APIRouter

from api.schemas import Replay, LabelResponse
from grl.classifier import classify
from grl.model_store import get_model_version

router = APIRouter()

@router.post("/label", response_model=LabelResponse, operation_id="label")
def label(replays: list[Replay]):
    replay_dicts = [item.model_dump() for item in replays]
    return {
        "model_version": get_model_version(),
        "results": classify(replay_dicts),
    }

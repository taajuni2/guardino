from fastapi import APIRouter, Depends
from fastapi_cli.cli import app
from sqlmodel import Session
from ..api.deps import get_db_session, get_current_user
from ..models.agent import Agent
from ..schemas.agent import AgentOut

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)

@router.get("/health")
async def health():
    return {"status": "ok"}
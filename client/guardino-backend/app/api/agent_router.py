from fastapi import APIRouter, Depends
from fastapi_cli.cli import app
from sqlmodel import Session
from ..api.deps import get_db_session, get_current_user
from ..models.agent import Agent
from ..schemas.agent import AgentOut

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

@router.get("/agents", response_model=list[AgentOut])
def list_agents(db: Session = Depends(get_db_session)):
    return db.query(Agent).all()
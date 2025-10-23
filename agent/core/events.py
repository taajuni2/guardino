# core/events.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
import uuid
from typing import List, Dict, Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Event:
    id: str
    timestamp: str
    agent_id: str
    type: str # "mass_creation" | "entropy_spike"
    severity: str # "info" | "warning" | "critical"
    summary: str
    paths: List[str]
    metadata: Dict[str, Any]
    raw: Dict[str, Any]

    @classmethod
    def build(
            cls,
            *,
            agent_id: str,
            type_: str,
            severity: str,
            summary: str,
            paths: list,
            metadata: dict,
            raw: dict | None = None,
    ) -> "Event":
        return cls(
            id=str(uuid.uuid4()),
            timestamp=now_iso(),
            agent_id=agent_id,
            type=type_,
            severity=severity,
            summary=summary,
            paths=paths,
            metadata=metadata,
            raw=raw or {},
        )

def to_dict(self):
    return asdict(self)

def to_json(self) -> str:
    return json.dumps(self.to_dict(), ensure_ascii=False)
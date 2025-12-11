# app/services/stats_service.py
from datetime import timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models  # du hast das ja schon so im Projekt


ONLINE_GRACE_MINUTES = 3  # Agent gilt als "online", wenn last_seen < 2 Min alt ist


async def get_agent_stats(db: AsyncSession) -> dict:
    """
    Aggregierte Statistiken zu Agents:
    - total_agents
    - online_agents
    - offline_agents
    """
    now = models.now_utc()
    threshold = now - timedelta(minutes=ONLINE_GRACE_MINUTES)

    # total agents
    total_q = select(func.count()).select_from(models.Agent)
    total_agents = (await db.execute(total_q)).scalar_one()

    # online agents (last_seen >= threshold)
    online_q = (
        select(func.count())
        .select_from(models.Agent)
        .where(models.Agent.last_seen >= threshold)
    )
    online_agents = (await db.execute(online_q)).scalar_one()

    offline_agents = total_agents - online_agents

    return {
        "total_agents": total_agents,
        "online_agents": online_agents,
        "offline_agents": offline_agents,
    }


async def get_threat_stats(db: AsyncSession) -> dict:
    """
    Aggregierte Statistiken zu Events / Threats.
    Annahme: event_type='alert' bedeutet "Threat detected".
    Passe das an, falls du andere event_type-Werte nutzt.
    """
    # Gesamtzahl aller Alerts
    total_alerts_q = (
        select(func.count())
        .select_from(models.Event)
        .where(models.Event.event_type == "alert")
    )
    total_alerts = (await db.execute(total_alerts_q)).scalar_one()

    # Alerts letzte 24h
    now = models.now_utc()
    last_24h = now - timedelta(hours=24)

    alerts_24h_q = (
        select(func.count())
        .select_from(models.Event)
        .where(
            and_(
                models.Event.event_type == "alert",
                models.Event.ts >= last_24h,
                )
        )
    )
    alerts_24h = (await db.execute(alerts_24h_q)).scalar_one()

    # Optional: nach Severity aufdröseln (critical / warning / info)
    by_severity_q = (
        select(models.Event.severity, func.count().label("cnt"))
        .select_from(models.Event)
        .where(models.Event.event_type == "alert")
        .group_by(models.Event.severity)
    )
    by_severity_result = await db.execute(by_severity_q)
    by_severity_raw = by_severity_result.all()

    by_severity = {
        (row.severity or "unknown"): row.cnt for row in by_severity_raw
    }

    return {
        "total_alerts": total_alerts,
        "alerts_last_24h": alerts_24h,
        "alerts_by_severity": by_severity,
    }

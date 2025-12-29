# app/main.py
import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.user_router import router as user_router
from .api.auth_router import router as auth_router
from .api.agent_router import router as agent_router
from .api.stats_router import router as stats_router
from .api.events_router import router as events_router
from .api.websocket_router import router as websocket_router
from .core.database import engine
from .services.kafka_consumer import consume_agent_messages

description = """
This backend processes all the event data sent by various agents from the Guardino System!  🚀

## Events

* You can **read Events from Kafka**. <br>
* You can search for specific EventID's.

"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    stop_event = asyncio.Event()
    consumer_task = asyncio.create_task(consume_agent_messages(stop_event))
    app.state.kafka_stop_event = stop_event
    app.state.kafka_task = consumer_task
    print("🚀 Kafka-Consumer gestartet...")
    # Fast API hook
    try:
        yield
    finally:
        # 2) Shutdownphase
        print("🛑 Kafka-Consumer wird gestoppt...")
        app.state.kafka_stop_event.set()
        # Task abbrechen, falls er noch irgendwo hängt
        app.state.kafka_task.cancel()
        try:
            await app.state.kafka_task
            await engine.dispose()
        except asyncio.CancelledError:
            pass
        print("✅ Kafka-Consumer gestoppt")

app = FastAPI(
    title="Client Backend",
    version="0.1.0",
    summary="This is the backend for the Guardino client application.",
    description=description,
    contact={
        "name": "Guardino Team",
        "email": "nicolas.julier@bluewin.ch"
    },
    lifespan=lifespan,
)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200").split(",")
print("Allowed Origins:", allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Frontend-URL
    allow_credentials=True,
    allow_methods=["*"],            # z. B. ['GET', 'POST']
    allow_headers=["*"],
)
stop_event = asyncio.Event()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(agent_router)
app.include_router(stats_router)
app.include_router(events_router)
app.include_router(websocket_router)

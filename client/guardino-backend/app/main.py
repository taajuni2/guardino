import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api.user_router import router as user_router
from .api.auth_router import router as auth_router
from .api.agent_router import router as agent_router
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
stop_event = asyncio.Event()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(agent_router)

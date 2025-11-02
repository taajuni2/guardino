from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api.user_router import router as user_router
from .api.auth_router import router as auth_router
from .core.database import engine

description = """
This backend processes all the event data sent by various agents from the Guardino System!  🚀

## Events

* You can **read Events from Kafka**. <br>
* You can search for specific EventID's.

"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    # Shutdown:
    await engine.dispose()

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

app.include_router(user_router)
app.include_router(auth_router)

import os
import sys
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

#
# Pfad anpassen, damit "import app" geht
#
project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from app.core.config import settings
from app.core.database import Base
from app import models  # noqa: F401 -> zwingt Import der Models, registriert Tabellen

# Alembic Config laden
config = context.config

# unsere DB_URL setzen (kann aus ENV kommen)
config.set_main_option("sqlalchemy.url", settings.DB_URL)

# Logging aktivieren
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# alle Models stecken in Base.metadata
target_metadata = Base.metadata
print("DEBUG TABLES:", list(target_metadata.tables.keys()))


def run_migrations_offline():
    """Erzeuge Migrationen ohne DB-Verbindung."""
    url = config.get_main_option("sqlalchemy.url")

    # compare_type=True -> erkennt Typänderungen
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    """Führe Migrationen mit echter DB-Connection aus."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Erzeuge/führe Migrationen mit echter DB-Connection (async)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as async_conn:
        await async_conn.run_sync(do_run_migrations)

    await connectable.dispose()


#




if context.is_offline_mode():
    # Wir generieren nur ein neues Skript -> kein echter DB-Connect nötig
    run_migrations_offline()
else:
    print("Alle Command")

    run_migrations_online()
    # Normale Welt:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())

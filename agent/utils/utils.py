# utils/utils.py
import yaml
import logging
import uuid
from pathlib import Path

log = logging.getLogger("agent.utils")


def load_config(path: str) -> dict:
    with open(path, "r") as file:
        config = yaml.safe_load(file)
        log.info("Successfully loaded config file")
        return config


def save_config(config: dict, path: str):
    with open(path, "w") as file:
        yaml.safe_dump(config, file)
    log.info("Updated config file with new values")


def get_or_create_agent_id(config_path: str) -> str:
    """
    Liest die agent_id aus der Konfiguration oder generiert sie neu.
    Schreibt sie zurück in das YAML-File, falls sie noch nicht existiert.
    """
    config_path = Path(config_path)
    config = load_config(config_path)

    agent_id = config.get("agent_id")

    if not agent_id or agent_id.strip() == "":
        # UUID erzeugen – du kannst hier auch "agent-" prefixen
        agent_id = f"agent-{uuid.uuid4()}"
        config["agent_id"] = agent_id
        save_config(config, config_path)
        log.info(f"Generated new agent_id: {agent_id}")
    else:
        log.info(f"Using existing agent_id: {agent_id}")

    return agent_id


def setup_logging(level="INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

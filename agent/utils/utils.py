import yaml
import logging

log = logging.getLogger("agent.utils")


def load_config(path: str) -> dict:
    """Lädt eine YAML-Konfigurationsdatei."""
    with open(path, 'r') as file:
        log.info("Sucessfully loaded config file")
        return yaml.safe_load(file)


def setup_logging(level="INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
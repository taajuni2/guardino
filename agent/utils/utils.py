import yaml


def load_config(path: str) -> dict:
    """Lädt eine YAML-Konfigurationsdatei."""
    with open(path, 'r') as file:
        return yaml.safe_load(file)
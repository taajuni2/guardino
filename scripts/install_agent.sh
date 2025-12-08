#!/usr/bin/env bash
set -euo pipefail

AGENT_USER="guardino-agent"
AGENT_GROUP="nogroup"
INSTALL_DIR="/opt/guardino/agent"
CONFIG_DIR="/etc/guardino"
CONFIG_FILE="${CONFIG_DIR}/agent_config.yaml"
SERVICE_FILE="/etc/systemd/system/guardino-agent.service"
VENV_DIR="${INSTALL_DIR}/venv"

echo "[*] Installing Guardino Agent..."

# In Repo-Root wechseln (von scripts/ eine Ebene hoch)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# 1. User anlegen (falls nicht vorhanden)
if ! id -u "${AGENT_USER}" >/dev/null 2>&1; then
  echo "[*] Creating system user ${AGENT_USER}..."
  useradd --system --no-create-home --shell /usr/sbin/nologin --gid "${AGENT_GROUP}" "${AGENT_USER}"
fi

# 2. Zielverzeichnis vorbereiten
echo "[*] Creating install dir ${INSTALL_DIR}..."
mkdir -p "${INSTALL_DIR}"
chown -R "${AGENT_USER}:${AGENT_GROUP}" "${INSTALL_DIR}"

# 3. Code in Install-Dir kopieren
echo "[*] Copying agent code to ${INSTALL_DIR}..."
if [ -d "${INSTALL_DIR}/backup" ]; then
  rm -rf "${INSTALL_DIR}/backup"
fi
if [ -d "${INSTALL_DIR}/current" ]; then
  mv "${INSTALL_DIR}/current" "${INSTALL_DIR}/backup"
fi

mkdir -p "${INSTALL_DIR}/current"

# komplettes Repo kopieren (inkl. agent/, certs/), aber ohne venv, .git usw.
rsync -a --delete \
  --exclude "venv" \
  --exclude ".git" \
  --exclude "__pycache__" \
  "${REPO_ROOT}/" "${INSTALL_DIR}/current/"

chown -R "${AGENT_USER}:${AGENT_GROUP}" "${INSTALL_DIR}"

# 4. venv erstellen + Requirements installieren
echo "[*] Creating virtualenv in ${VENV_DIR}..."
python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/pip" install --upgrade pip

REQ_FILE="${INSTALL_DIR}/current/agent/requirements.txt"
if [ -f "${REQ_FILE}" ]; then
  echo "[*] Installing Python dependencies from ${REQ_FILE}..."
  "${VENV_DIR}/bin/pip" install -r "${REQ_FILE}"
else
  echo "[!] WARNING: requirements.txt not found at ${REQ_FILE}, skipping pip install."
fi

# 5. Config anlegen, falls nicht vorhanden
echo "[*] Ensuring config in ${CONFIG_FILE}..."
mkdir -p "${CONFIG_DIR}"
if [ ! -f "${CONFIG_FILE}" ]; then
  echo "[*] Creating default config file..."
  cat > "${CONFIG_FILE}" <<EOF
# Guardino Agent config (default)
agent_version: "0.1.0"
agent_id: ""
watch_directories:
  - "/home/vmadmin/test"

blacklist_paths:
  - "/proc"
  - "/sys"
  - "/dev"
  - "/tmp"

kafka:
  broker: "192.168.110.60:9092"
  topics:
    events: "agent-events"
    control: "agent-lifecycle"


heartbeat_interval_s: 60

log_level: "INFO"



EOF
  chown "${AGENT_USER}:${AGENT_GROUP}" "${CONFIG_FILE}"
  chmod 640 "${CONFIG_FILE}"
else
  echo "[*] Existing config found, not overwriting."
fi

# 6. systemd Unit schreiben
echo "[*] Writing systemd service to ${SERVICE_FILE}..."

cat > "${SERVICE_FILE}" <<EOF
[Unit]
Description=Guardino Ransomware Detection Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${AGENT_USER}
Group=${AGENT_GROUP}
WorkingDirectory=${INSTALL_DIR}/current

Environment="PYTHONUNBUFFERED=1"
Environment="AGENT_CONFIG=${CONFIG_FILE}"

# WICHTIG: Dein Package heißt 'agent', main liegt in agent/main.py
ExecStart=${VENV_DIR}/bin/python -m agent.main

Restart=always
RestartSec=5

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 7. systemd neu laden und Service aktivieren
echo "[*] Reloading systemd and enabling service..."
systemctl daemon-reload
systemctl enable --now guardino-agent

echo "[*] Installation complete. Service status:"
systemctl --no-pager --full status guardino-agent || true

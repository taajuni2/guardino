#!/usr/bin/env bash
set -euo pipefail

SERVICE_FILE="/etc/systemd/system/guardino-agent.service"
INSTALL_DIR="/opt/guardino/agent"
CONFIG_DIR="/etc/guardino"
AGENT_USER="guardino-agent"

echo "[*] Stopping service..."
systemctl stop guardino-agent || true
systemctl disable guardino-agent || true

echo "[*] Removing systemd unit..."
rm -f "${SERVICE_FILE}"
systemctl daemon-reload || true

echo "[*] Removing installation directory..."
rm -rf "${INSTALL_DIR}"

echo "[*] Removing config directory (optional)..."
rm -rf "${CONFIG_DIR}"

echo "[*] Removing agent user..."
if id "${AGENT_USER}" >/dev/null 2>&1; then
  userdel "${AGENT_USER}"
fi

echo "[*] Uninstallation complete."

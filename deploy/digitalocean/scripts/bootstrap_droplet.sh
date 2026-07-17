#!/usr/bin/env bash
# Bootstrap Ubuntu Droplet para jean piaget IA. Ejecutar como root.
set -euo pipefail

APP_USER="${APP_USER:-www-data}"
APP_ROOT="${APP_ROOT:-/var/www/piaget}"
APP_DIR="${APP_DIR:-${APP_ROOT}/app}"

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y python3 python3-venv python3-pip nginx git curl

mkdir -p "$APP_ROOT" "$APP_DIR" "${APP_DIR}/logs" "${APP_DIR}/media" "${APP_DIR}/db"
chown -R "${APP_USER}:${APP_USER}" "$APP_ROOT"

if [ ! -d "${APP_DIR}/venv" ]; then
  sudo -u "$APP_USER" python3 -m venv "${APP_DIR}/venv"
fi

if [ -f "${APP_DIR}/requirements.txt" ]; then
  sudo -u "$APP_USER" bash -c "
    source '${APP_DIR}/venv/bin/activate'
    pip install --upgrade pip
    pip install -r '${APP_DIR}/requirements.txt'
  "
fi

install -m 644 "${APP_DIR}/deploy/digitalocean/nginx/piaget.conf" /etc/nginx/sites-available/piaget
ln -sf /etc/nginx/sites-available/piaget /etc/nginx/sites-enabled/piaget
rm -f /etc/nginx/sites-enabled/default
nginx -t

install -m 644 "${APP_DIR}/deploy/digitalocean/systemd/piaget.service" /etc/systemd/system/piaget.service
systemctl daemon-reload

echo "Bootstrap listo. Configure .env y ejecute deploy.sh"

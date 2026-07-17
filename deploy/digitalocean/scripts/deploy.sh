#!/usr/bin/env bash
# Actualiza jean piaget IA en el droplet. Ejecutar desde APP_DIR como root o con sudo.
set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/piaget/app}"
APP_USER="${APP_USER:-www-data}"
cd "$APP_DIR"

if [ -d .git ]; then
  sudo -u "$APP_USER" git fetch origin
  sudo -u "$APP_USER" git reset --hard origin/main
fi

sudo -u "$APP_USER" bash -c "
  source '${APP_DIR}/venv/bin/activate'
  set -a
  [ -f '${APP_DIR}/.env' ] && . '${APP_DIR}/.env'
  set +a
  pip install -r requirements.txt
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  python manage.py ensure_neo
"

systemctl restart piaget
systemctl reload nginx
echo "Deploy OK — http://67.205.138.3/"

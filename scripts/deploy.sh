#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
#  deploy.sh — Full DigitalOcean Basic Droplet deployment
#  Ubuntu 22.04 LTS · Django 5 · PostgreSQL · Nginx · Gunicorn · SSL
#
#  Usage (as root on a fresh droplet):
#    chmod +x deploy.sh
#    ./deploy.sh yourdomain.com your@email.com
#
#  After first run, use: ./deploy.sh --update   to deploy new code only
# ═══════════════════════════════════════════════════════════════════════
set -euo pipefail

DOMAIN="${1:-yourdomain.com}"
EMAIL="${2:-admin@example.com}"
APP_USER="portfolio"
APP_DIR="/home/${APP_USER}/app"
VENV_DIR="/home/${APP_USER}/venv"
REPO_URL="https://github.com/basantasingh/portfolio.git"   # ← update this

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
log()  { echo -e "${GREEN}[deploy]${NC} $*"; }
warn() { echo -e "${YELLOW}[warn]${NC}  $*"; }
err()  { echo -e "${RED}[error]${NC} $*"; exit 1; }

# ── Update-only mode ────────────────────────────────────────────────
if [[ "${1:-}" == "--update" ]]; then
  log "Running update deploy..."
  cd "$APP_DIR"
  sudo -u "$APP_USER" git pull origin main
  sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install -r requirements/production.txt -q
  sudo -u "$APP_USER" "$VENV_DIR/bin/python" manage.py migrate --settings=config.settings.production
  sudo -u "$APP_USER" "$VENV_DIR/bin/python" manage.py collectstatic --noinput --settings=config.settings.production
  systemctl restart portfolio
  log "Update complete."
  exit 0
fi

# ════════════════════════════════════════════════════════════════════════
# FULL INSTALL
# ════════════════════════════════════════════════════════════════════════

[[ $EUID -ne 0 ]] && err "Run as root: sudo ./deploy.sh"

log "=== Step 1/10: System update ==="
apt-get update -qq && apt-get upgrade -y -qq

log "=== Step 2/10: Install packages ==="
apt-get install -y -qq \
  python3 python3-pip python3-venv python3-dev \
  postgresql postgresql-contrib \
  nginx certbot python3-certbot-nginx \
  git curl build-essential \
  libpq-dev libjpeg-dev libpng-dev zlib1g-dev \
  fail2ban ufw

log "=== Step 3/10: Create app user ==="
id "$APP_USER" &>/dev/null || useradd -m -s /bin/bash "$APP_USER"
usermod -aG www-data "$APP_USER"

log "=== Step 4/10: Configure PostgreSQL ==="
DB_PASS=$(openssl rand -base64 24 | tr -dc 'A-Za-z0-9' | head -c 32)
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='${APP_USER}'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE USER ${APP_USER} WITH PASSWORD '${DB_PASS}';"
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='portfolio_db'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE DATABASE portfolio_db OWNER ${APP_USER};"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO ${APP_USER};"
log "DB password: ${DB_PASS}  (save this!)"

log "=== Step 5/10: Clone repo & virtualenv ==="
mkdir -p "$APP_DIR"
if [[ -d "$APP_DIR/.git" ]]; then
  sudo -u "$APP_USER" git -C "$APP_DIR" pull origin main
else
  sudo -u "$APP_USER" git clone "$REPO_URL" "$APP_DIR"
fi

sudo -u "$APP_USER" python3 -m venv "$VENV_DIR"
sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install --upgrade pip -q
sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements/production.txt" -q

log "=== Step 6/10: Environment file ==="
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
if [[ ! -f "$APP_DIR/.env" ]]; then
cat > "$APP_DIR/.env" <<EOF
DJANGO_SECRET_KEY=${SECRET_KEY}
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=${DOMAIN},www.${DOMAIN}
DATABASE_URL=postgres://${APP_USER}:${DB_PASS}@localhost:5432/portfolio_db
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=mailbasantasingh@gmail.com
EMAIL_HOST_PASSWORD=REPLACE_WITH_APP_PASSWORD
DEFAULT_FROM_EMAIL=noreply@${DOMAIN}
CONTACT_EMAIL=mailbasantasingh@gmail.com
ADMIN_URL=secure-admin-$(openssl rand -hex 6)/
SENTRY_DSN=
EOF
  chown "$APP_USER:$APP_USER" "$APP_DIR/.env"
  chmod 600 "$APP_DIR/.env"
  warn ".env created — edit EMAIL_HOST_PASSWORD before going live!"
fi

log "=== Step 7/10: Django setup ==="
mkdir -p /var/log/portfolio /var/cache/portfolio /run/portfolio
chown "$APP_USER:$APP_USER" /var/log/portfolio /var/cache/portfolio
chown "$APP_USER:www-data" /run/portfolio
chmod 775 /run/portfolio

DJANGO_CMD="$VENV_DIR/bin/python $APP_DIR/manage.py"
DJANGO_SETTINGS="--settings=config.settings.production"

sudo -u "$APP_USER" $DJANGO_CMD migrate $DJANGO_SETTINGS
sudo -u "$APP_USER" $DJANGO_CMD collectstatic --noinput $DJANGO_SETTINGS
sudo -u "$APP_USER" $DJANGO_CMD check --deploy $DJANGO_SETTINGS || warn "Deploy check warnings (review above)"

log "=== Step 8/10: Systemd services ==="
cp "$APP_DIR/scripts/portfolio.service" /etc/systemd/system/
cp "$APP_DIR/scripts/portfolio.socket"  /etc/systemd/system/

# Update paths in service file
sed -i "s|/home/portfolio/app|${APP_DIR}|g" /etc/systemd/system/portfolio.service
sed -i "s|/home/portfolio/venv|${VENV_DIR}|g" /etc/systemd/system/portfolio.service

systemctl daemon-reload
systemctl enable portfolio.socket portfolio
systemctl start  portfolio.socket portfolio

log "=== Step 9/10: Nginx ==="
# Add rate limit zone to nginx.conf http block
grep -q "limit_req_zone" /etc/nginx/nginx.conf || \
  sed -i '/http {/a\\tlimit_req_zone $binary_remote_addr zone=contact:10m rate=5r/m;' /etc/nginx/nginx.conf

cp "$APP_DIR/scripts/nginx.conf" /etc/nginx/sites-available/portfolio
sed -i "s/yourdomain.com/${DOMAIN}/g" /etc/nginx/sites-available/portfolio
ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

log "=== Step 10/10: SSL with Certbot ==="
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive \
  --agree-tos --email "$EMAIL" --redirect || warn "SSL setup failed — run manually: certbot --nginx -d $DOMAIN"

# Auto-renew cron
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && systemctl reload nginx") | crontab -

log "=== Firewall ==="
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

log "=== fail2ban ==="
systemctl enable fail2ban
systemctl start  fail2ban

# ── Print summary ────────────────────────────────────────────
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Deployment complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo "  Site URL    : https://${DOMAIN}"
echo "  App dir     : ${APP_DIR}"
echo "  Logs        : /var/log/portfolio/"
echo "  DB password : ${DB_PASS}"
echo ""
echo "  Next steps:"
echo "  1. Edit ${APP_DIR}/.env — set EMAIL_HOST_PASSWORD"
echo "  2. Create superuser: sudo -u ${APP_USER} ${VENV_DIR}/bin/python ${APP_DIR}/manage.py createsuperuser --settings=config.settings.production"
echo "  3. Visit /admin → add Site Profile, Teaching subjects, Projects"
echo ""

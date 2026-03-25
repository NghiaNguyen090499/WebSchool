#!/usr/bin/env bash
# =============================================================================
# MIS Website - Production deployment script
# =============================================================================
# Usage: bash deploy/deploy.sh [first|update|rollback|smoke|backup]
# =============================================================================

set -euo pipefail

APP_DIR="/opt/mis-website"
ENV_FILE="$APP_DIR/.env"
VENV="$APP_DIR/venv"
PYTHON="$VENV/bin/python"
PIP="$VENV/bin/pip"
SERVICE="mis-website"
DEPLOY_BRANCH="${DEPLOY_BRANCH:-main}"
BACKUP_DIR="/opt/backups/mis-website"
MEDIA_BACKUP_DIR="$BACKUP_DIR/media"
GUNICORN_SOCKET="/run/gunicorn/mis-website.sock"
NGINX_SITE="/etc/nginx/sites-available/mis-website"
NGINX_LINK="/etc/nginx/sites-enabled/mis-website"
CERTBOT_WEBROOT="/var/www/certbot"
PRIMARY_DOMAIN="misvn.edu.vn"
SECONDARY_DOMAIN="www.misvn.edu.vn"
CERT_PATH="/etc/letsencrypt/live/$PRIMARY_DOMAIN/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/$PRIMARY_DOMAIN/privkey.pem"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[DEPLOY]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1" >&2; }

check_env() {
    if [ ! -f "$ENV_FILE" ]; then
        err ".env file not found at $ENV_FILE"
        exit 1
    fi
    log ".env file found"
}

load_env() {
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a

    if [ -n "${SMOKE_HOST:-}" ]; then
        APP_SMOKE_HOST="$SMOKE_HOST"
        return
    fi

    local host
    local hosts_string="${ALLOWED_HOSTS:-}"
    IFS=',' read -ra hosts <<< "$hosts_string"
    for host in "${hosts[@]}"; do
        host="${host// /}"
        case "$host" in
            ""|localhost|127.0.0.1|0.0.0.0|"[::1]")
                ;;
            *)
                APP_SMOKE_HOST="$host"
                return
                ;;
        esac
    done
    APP_SMOKE_HOST="localhost"
}

validate_bool() {
    local name="$1"
    local value="${!name:-}"
    case "$value" in
        True|False|true|false|1|0|yes|no|on|off)
            ;;
        *)
            err "$name must be a boolean-like value. Received: ${value:-<empty>}"
            exit 1
            ;;
    esac
}

validate_env() {
    validate_bool DEBUG

    case "${DEBUG:-}" in
        False|false|0|off|OFF|no|NO)
            ;;
        *)
            err "Production deploy requires DEBUG=False in $ENV_FILE"
            exit 1
            ;;
    esac

    if [ -z "${SECRET_KEY:-}" ] || [[ "${SECRET_KEY}" == django-insecure-* ]]; then
        err "SECRET_KEY is missing or still using the development placeholder."
        exit 1
    fi

    if [ -z "${ALLOWED_HOSTS:-}" ]; then
        err "ALLOWED_HOSTS must be configured."
        exit 1
    fi

    if [ -z "${DATABASE_URL:-}" ]; then
        warn "DATABASE_URL is empty. Deployment will fall back to DB_* settings."
    fi
}

ensure_directories() {
    mkdir -p "$APP_DIR/logs" "$APP_DIR/media" "$APP_DIR/staticfiles" "$BACKUP_DIR" "$MEDIA_BACKUP_DIR"
    sudo mkdir -p "$CERTBOT_WEBROOT"
    sudo chown -R www-data:www-data "$APP_DIR/logs" "$APP_DIR/media" "$APP_DIR/staticfiles"
}

ensure_virtualenv() {
    if [ ! -d "$VENV" ]; then
        log "Creating virtual environment"
        python3 -m venv "$VENV"
    fi
}

backup_db() {
    mkdir -p "$BACKUP_DIR"
    local backup_file="$BACKUP_DIR/db_$(date +%Y%m%d_%H%M%S).sql.gz"
    log "Backing up database to $backup_file"

    if [ -n "${DATABASE_URL:-}" ]; then
        pg_dump "$DATABASE_URL" | gzip > "$backup_file"
        log "Database backup complete"
    else
        warn "DATABASE_URL not set, skipping DB backup"
    fi

    ls -t "$BACKUP_DIR"/db_*.sql.gz 2>/dev/null | tail -n +8 | xargs -r rm
}

backup_media() {
    mkdir -p "$MEDIA_BACKUP_DIR"
    local media_file="$MEDIA_BACKUP_DIR/media_$(date +%Y%m%d).tar.gz"

    if [ ! -f "$media_file" ]; then
        log "Creating media backup $media_file"
        tar -czf "$media_file" -C "$APP_DIR" media/ 2>/dev/null || true
    else
        log "Media backup for today already exists"
    fi
}

pull_code() {
    log "Pulling latest code from origin/$DEPLOY_BRANCH"
    cd "$APP_DIR"
    git fetch origin "$DEPLOY_BRANCH"
    git checkout -B "$DEPLOY_BRANCH" "origin/$DEPLOY_BRANCH"
}

install_deps() {
    log "Installing Python dependencies"
    "$PIP" install -r "$APP_DIR/requirements.txt" --quiet
}

django_check() {
    log "Running Django checks"
    (cd "$APP_DIR" && "$PYTHON" manage.py check)
    (cd "$APP_DIR" && "$PYTHON" manage.py check --deploy)
}

django_migration_check() {
    log "Checking for pending model changes"
    (cd "$APP_DIR" && "$PYTHON" manage.py makemigrations --check --dry-run)
}

django_migrate() {
    log "Running migrations"
    (cd "$APP_DIR" && "$PYTHON" manage.py migrate --noinput)
}

django_collectstatic() {
    log "Collecting static files"
    (cd "$APP_DIR" && "$PYTHON" manage.py collectstatic --noinput --clear)
}

django_compilemessages() {
    if [ ! -d "$APP_DIR/locale" ]; then
        log "No locale directory detected, skipping compilemessages"
        return
    fi

    if ! find "$APP_DIR/locale" -name "*.po" -print -quit | grep -q .; then
        log "No translation catalogs detected, skipping compilemessages"
        return
    fi

    if ! command -v msgfmt >/dev/null 2>&1; then
        err "gettext/msgfmt is required to compile translations."
        exit 1
    fi

    log "Compiling translation messages"
    (cd "$APP_DIR" && "$PYTHON" manage.py compilemessages)
}

sync_systemd_service() {
    log "Installing systemd service"
    sudo cp "$APP_DIR/deploy/gunicorn.service" "/etc/systemd/system/$SERVICE.service"
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE"
}

install_bootstrap_nginx_config() {
    log "Installing temporary HTTP-only Nginx config"
    sudo tee "$NGINX_SITE" >/dev/null <<EOF
limit_req_zone \$binary_remote_addr zone=mis_forms:10m rate=10r/m;

server {
    listen 80;
    listen [::]:80;
    server_name $PRIMARY_DOMAIN $SECONDARY_DOMAIN;

    location /.well-known/acme-challenge/ {
        root $CERTBOT_WEBROOT;
    }

    location / {
        proxy_pass http://unix:$GUNICORN_SOCKET;
        proxy_set_header Host              \$host;
        proxy_set_header X-Real-IP         \$remote_addr;
        proxy_set_header X-Forwarded-For   \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    sudo ln -sf "$NGINX_SITE" "$NGINX_LINK"
    sudo nginx -t
    sudo systemctl reload nginx
}

install_full_nginx_config() {
    log "Installing full Nginx config"
    sudo cp "$APP_DIR/deploy/nginx.conf" "$NGINX_SITE"
    sudo ln -sf "$NGINX_SITE" "$NGINX_LINK"
    sudo nginx -t
    sudo systemctl reload nginx
}

ensure_certificate() {
    if [ -f "$CERT_PATH" ] && [ -f "$KEY_PATH" ]; then
        log "TLS certificate already present"
        return
    fi

    if ! command -v certbot >/dev/null 2>&1; then
        err "certbot is not installed."
        exit 1
    fi

    install_bootstrap_nginx_config

    log "Requesting Let's Encrypt certificate"
    sudo certbot certonly --webroot \
        -w "$CERTBOT_WEBROOT" \
        -d "$PRIMARY_DOMAIN" \
        -d "$SECONDARY_DOMAIN"
}

restart_gunicorn() {
    log "Restarting Gunicorn"
    sudo systemctl restart "$SERVICE"
    sleep 2

    if sudo systemctl is-active --quiet "$SERVICE"; then
        log "Gunicorn is running"
    else
        err "Gunicorn failed to start"
        sudo journalctl -u "$SERVICE" --no-pager -n 50
        exit 1
    fi
}

socket_request() {
    local path="$1"
    local expected="$2"
    local status

    status=$(curl --silent --show-error --output /dev/null \
        --write-out "%{http_code}" \
        --unix-socket "$GUNICORN_SOCKET" \
        -H "Host: $APP_SMOKE_HOST" \
        "http://localhost$path")

    if [ "$status" = "$expected" ]; then
        echo "  OK  socket $path -> $status"
    else
        echo "  ERR socket $path -> $status (expected $expected)"
        return 1
    fi
}

https_request() {
    local path="$1"
    local expected="$2"
    local status

    status=$(curl --silent --show-error --output /dev/null \
        --write-out "%{http_code}" \
        --resolve "$APP_SMOKE_HOST:443:127.0.0.1" \
        "https://$APP_SMOKE_HOST$path")

    if [ "$status" = "$expected" ]; then
        echo "  OK  https  $path -> $status"
    else
        echo "  ERR https  $path -> $status (expected $expected)"
        return 1
    fi
}

smoke_test() {
    local fail=0
    log "Running smoke tests against Gunicorn socket"

    for path in "/" "/en/" "/news/" "/events/" "/gallery/" "/tuyen-sinh/" "/contact/" "/healthz/" "/readyz/"; do
        socket_request "$path" "200" || fail=1
    done
    socket_request "/portal/" "302" || fail=1
    socket_request "/admin/" "302" || fail=1

    if [ -f "$CERT_PATH" ] && [ -f "$KEY_PATH" ]; then
        log "Running smoke tests through local HTTPS/Nginx"
        https_request "/healthz/" "200" || fail=1
        https_request "/readyz/" "200" || fail=1
    else
        warn "TLS certificate not present yet, skipping HTTPS smoke tests"
    fi

    if [ "$fail" -ne 0 ]; then
        err "Smoke tests failed"
        exit 1
    fi
}

create_superuser_hint() {
    log "Create an admin account if needed:"
    echo "  cd $APP_DIR && $PYTHON manage.py createsuperuser"
}

first_setup() {
    log "=== FIRST-TIME SETUP ==="
    ensure_directories
    ensure_virtualenv
    install_deps
    django_check
    django_migration_check
    django_migrate
    django_collectstatic
    django_compilemessages
    sync_systemd_service
    restart_gunicorn
    ensure_certificate
    install_full_nginx_config
    smoke_test
    create_superuser_hint
    log "=== FIRST-TIME SETUP COMPLETE ==="
}

update_deploy() {
    log "=== UPDATE DEPLOY ==="
    backup_db
    backup_media
    pull_code
    ensure_directories
    ensure_virtualenv
    install_deps
    django_check
    django_migration_check
    django_migrate
    django_collectstatic
    django_compilemessages
    sync_systemd_service
    install_full_nginx_config
    restart_gunicorn
    smoke_test
    log "=== UPDATE DEPLOY COMPLETE ==="
}

rollback() {
    local target_commit="${2:-$(cd "$APP_DIR" && git rev-parse HEAD^)}"
    log "=== ROLLBACK TO $target_commit ==="
    backup_db
    backup_media
    cd "$APP_DIR"
    git checkout -B "$DEPLOY_BRANCH" "$target_commit"
    ensure_directories
    install_deps
    django_check
    django_migrate
    django_collectstatic
    django_compilemessages
    sync_systemd_service
    install_full_nginx_config
    restart_gunicorn
    smoke_test
    log "=== ROLLBACK COMPLETE ==="
}

check_env
load_env
validate_env

case "${1:-update}" in
    first)
        first_setup
        ;;
    update)
        update_deploy
        ;;
    rollback)
        rollback "$@"
        ;;
    smoke)
        smoke_test
        ;;
    backup)
        backup_db
        backup_media
        ;;
    *)
        echo "Usage: $0 [first|update|rollback|smoke|backup]"
        exit 1
        ;;
esac

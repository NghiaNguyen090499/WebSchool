#!/usr/bin/env bash
# =============================================================================
# MIS Website — Database Backup (Cron job)
# =============================================================================
# Install:
#   crontab -e
#   0 2 * * * /opt/mis-website/deploy/backup.sh >> /opt/mis-website/logs/backup.log 2>&1
# =============================================================================

set -euo pipefail

APP_DIR="/opt/mis-website"
BACKUP_DIR="/opt/backups/mis-website"
MEDIA_BACKUP_DIR="/opt/backups/mis-website/media"
RETENTION_DAYS=30

mkdir -p "$BACKUP_DIR" "$MEDIA_BACKUP_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting backup ..."

# ─── Database backup ───
source "$APP_DIR/.env"
if [ -n "${DATABASE_URL:-}" ]; then
    DB_FILE="$BACKUP_DIR/db_$(date +%Y%m%d_%H%M%S).sql.gz"
    pg_dump "$DATABASE_URL" | gzip > "$DB_FILE"
    echo "  DB backup: $DB_FILE ($(du -h "$DB_FILE" | cut -f1))"
fi

# ─── Media files backup (incremental) ───
MEDIA_FILE="$MEDIA_BACKUP_DIR/media_$(date +%Y%m%d).tar.gz"
if [ ! -f "$MEDIA_FILE" ]; then
    tar -czf "$MEDIA_FILE" -C "$APP_DIR" media/ 2>/dev/null || true
    echo "  Media backup: $MEDIA_FILE ($(du -h "$MEDIA_FILE" | cut -f1))"
else
    echo "  Media backup: already done today"
fi

# ─── Cleanup old backups ───
find "$BACKUP_DIR" -name "db_*.sql.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null
find "$MEDIA_BACKUP_DIR" -name "media_*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup complete ✓"

#!/bin/bash
set -euo pipefail

ARCHIVE="cloudfronts-site.tar.gz"
TARGET="/var/www/html"
BACKUP="/var/www/html-backup-$(date +%Y%m%d-%H%M%S)"

if [ ! -f "$ARCHIVE" ]; then
  echo "Error: $ARCHIVE not found. Place it alongside this script."
  exit 1
fi

if [ "$EUID" -ne 0 ]; then
  echo "Error: This script must be run as root (sudo)."
  exit 1
fi

echo "[1/6] Stopping Apache gracefully ..."
apachectl graceful-stop || systemctl stop apache2 || /etc/init.d/apache2 stop || true

echo "[2/6] Creating backup of current site at $BACKUP ..."
cp -a "$TARGET" "$BACKUP"

echo "[3/6] Removing all files under $TARGET ..."
rm -rf "$TARGET"/* "$TARGET"/.??* 2>/dev/null || true

echo "[4/6] Extracting $ARCHIVE to $TARGET ..."
tar xzf "$ARCHIVE" -C "$TARGET"

echo "[5/6] Cleaning Apple Double resource fork files ..."
find "$TARGET" -name '._*' -type f -delete

echo "[6/6] Setting ownership to www:www ..."
chown -R www:www "$TARGET"

echo "[7/7] Restarting Apache ..."
apachectl restart || systemctl restart apache2 || /etc/init.d/apache2 restart || true

echo "Done. Backup saved at $BACKUP"
ls -la "$TARGET" | head -20

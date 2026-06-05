#!/bin/bash
# Deploy script for cloudfrontsgroup.org
# Usage: ./deploy.sh "commit message"

set -e

if [ -z "$1" ]; then
  echo "Usage: ./deploy.sh \"commit message\""
  exit 1
fi

git add -A
git commit -m "$1"
git push

echo "✓ Deployed to GitHub Pages"
echo "  https://cloudfrontsgroup.org"

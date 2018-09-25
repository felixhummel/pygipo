#!/bin/bash
set -euo pipefail

log() { echo "$@" 2>&1; }
warn() { log "WARNING $@"; }

[[ ! -f .env ]] && ./bin/generate_env_file.sh > .env || warn ".env exists. skipping"

# Link `docker-compose.override.yml` to base dir:
[[ -f docker-compose.override.yml ]] || ln -s env/dev/docker-compose.override.yml

docker-compose build

docker-compose up -d postgres
docker-compose run --rm app ./manage.py wait_for_db

docker-compose run --rm app ./manage.py migrate

docker-compose up -d

# print possible next steps
cat <<'EOF'

http://localhost:8000
docker-compose logs -f
EOF

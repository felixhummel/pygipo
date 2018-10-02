#!/bin/bash
set -euo pipefail

cat <<EOF
COMPOSE_UID=$(id -u)
COMPOSE_GID=$(id -g)

DJANGO_SECRET_KEY=$(pwgen 32 1)
GITLAB_URL=
GITLAB_PRIVATE_TOKEN=
EOF

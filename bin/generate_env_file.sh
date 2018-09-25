#!/bin/bash
set -euo pipefail

cat <<EOF
COMPOSE_UID=$(id -u)
COMPOSE_GID=$(id -g)
EOF

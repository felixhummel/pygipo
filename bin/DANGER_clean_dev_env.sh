#!/bin/bash
set -euo pipefail

docker-compose down --remove-orphans
volumes=$(docker volume ls -q --filter label=de.felixhummel.project=pygipo)
[[ -n $volumes ]] && docker volume rm $volumes

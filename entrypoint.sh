#!/bin/bash
set -euo pipefail

cat <<EOF > ~/.python-gitlab.cfg
[global]
default = default
timeout = 5

[default]
url = $GITLAB_URL
private_token = $GITLAB_PRIVATE_TOKEN
EOF

exec $@

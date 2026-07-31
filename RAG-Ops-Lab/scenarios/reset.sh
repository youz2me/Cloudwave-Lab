#!/usr/bin/env bash
set -euo pipefail

curl -s -X DELETE localhost:8000/admin/fault > /dev/null
echo "장애 주입 해제 완료. 지표가 평시로 돌아오는지까지 확인해야 복구다."

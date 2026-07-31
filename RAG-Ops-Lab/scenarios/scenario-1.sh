#!/usr/bin/env bash
set -euo pipefail

curl -s -X POST localhost:8000/admin/fault/f1 > /dev/null

echo "[시나리오 1] 주입 완료."
echo
echo "온콜 폰이 울릴 것이다. 무슨 일이 벌어졌는지는 관측으로 알아내라."
echo "  - Prometheus 알림: http://localhost:9090/alerts"
echo "  - 다 봤으면 네 어시스턴트에게 물어봐라. 문서에 답이 있는가?"
echo
echo "복구: scenarios/reset.sh"

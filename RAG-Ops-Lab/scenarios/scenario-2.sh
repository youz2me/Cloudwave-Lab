#!/usr/bin/env bash
set -euo pipefail

curl -s -X POST localhost:8000/admin/fault/f2 > /dev/null

echo "[시나리오 2] 주입 완료."
echo
echo "CS 채널 제보: \"결제가 안 됐다는 문의가 몇 건 들어왔어요.\""
echo "무슨 일인지, 뭘 해야 하는지는 네가 판단한다."
echo "  - Prometheus 알림: http://localhost:9090/alerts"
echo "  - 네 어시스턴트는 이 상황에 쓸모가 있는가? 없다면 왜인가?"
echo
echo "복구: scenarios/reset.sh"

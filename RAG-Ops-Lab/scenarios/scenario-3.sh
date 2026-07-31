#!/usr/bin/env bash
set -euo pipefail

curl -s -X POST localhost:8000/admin/fault/f3 > /dev/null

echo "[시나리오 3] 주입 완료."
echo
echo "고객센터 제보: \"예매번호가 다른 사람이랑 똑같이 나왔다는 항의가 들어왔어요.\""
echo "알림은 조용하다. 그게 이 시나리오의 전부다."
echo "  - 직접 확인해봐라: curl localhost:8000/book"
echo "  - 네 어시스턴트에게 물어봐라. 그리고 그 답을 그대로 믿어도 되는지 판단해라."
echo
echo "복구: scenarios/reset.sh"

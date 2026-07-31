"""평시 트래픽 발생기.

이 실습의 주인공은 부하가 아니라 '운영 지식'이다. 그래서 부하는 미리 깔아준다.
- /browse ~10 rps, /book ~6 rps. 평시엔 아무 알림도 울리지 않는 수준.
"""

import os
import random
import threading
import time
import urllib.request

BASE = os.getenv("TARGET", "http://app:8000")


def hit(path: str) -> None:
    try:
        urllib.request.urlopen(BASE + path, timeout=5).read()
    except Exception:
        pass  # 실패도 서버 지표에는 남는다. 여기서는 조용히 넘어간다.


def worker(path: str, rps: float) -> None:
    interval = 1.0 / rps
    while True:
        threading.Thread(target=hit, args=(path,), daemon=True).start()
        time.sleep(interval * random.uniform(0.7, 1.3))


if __name__ == "__main__":
    threading.Thread(target=worker, args=("/browse", 10.0), daemon=True).start()
    worker("/book", 6.0)

# 런북: 예매 지연 (BookingLatencyHigh)

- 대상 알림: `BookingLatencyHigh` — `/book` P95 > 0.5s, 1분 지속
- 최종 수정: 2026-03-21, 서태오

## 1. 지금 실제로 느린가부터 확인한다

```promql
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{route="/book"}[1m])))
```

- 순간 스파이크 한 번인지, 지속 중인지 구분한다. 지속 중이면 다음으로.

## 2. 범위를 좁힌다: 앱 전체인가, 예매 경로만인가

```promql
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{route="/browse"}[1m])))
```

- `/browse`도 같이 느리다 → 앱/호스트 수준 문제. 3-A로.
- `/book`만 느리다 → 예매 경로(DB 커넥션 풀 포함) 문제. 3-B로.

## 3-A. 앱 전체가 느릴 때

- `process_cpu_seconds_total` 증가율, `process_resident_memory_bytes` 확인
- 앱 로그(`docker compose logs app`)에서 에러/재시작 흔적 확인

## 3-B. 예매 경로만 느릴 때

```promql
db_pool_waiters
db_pool_connections_in_use
```

- `in_use`가 풀 크기에 고정 + `waiters` > 0 지속 → 풀 고갈.
  `runbooks/db-connection-pool.md`로 이동.
- 풀은 여유 있는데 느리다 → DB 자체 지연 의심. DB 로그 확인 후 에스컬레이션.

## 4. 조치 원칙

- 원인을 모르는 단계에서의 조치는 **가역적인 것만** 한다.
  (유입 완화, 대기 페이지 활성화는 가역. 근거 없는 재시작·데이터 삭제는 금지.)
- 조치 전후로 1번 쿼리 값을 기록해 조치 효과를 숫자로 남긴다.

## 5. 에스컬레이션

- 15분 안에 원인 범위를 못 좁히면 플랫폼 리드 호출. 혼자 붙들지 않는다.

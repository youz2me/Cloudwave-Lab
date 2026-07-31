# 알림 카탈로그

최종 수정: 2026-03-21, 김한결

운영 중인 Prometheus 알림 전체 목록. 임계값을 바꿀 때는 반드시 근거를 함께 수정한다.

## BookingLatencyHigh

- 조건: `/book` P95 > 0.5초, 1분 지속
- 식: `histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{route="/book"}[1m]))) > 0.5`
- 임계값 근거: CS 문의 데이터 기준, 예매 응답이 0.5초를 넘기 시작하면
  "안 되는 것 같다"는 문의가 유의미하게 늘었다 (2026-01 조사).
- 첫 대응: `runbooks/high-latency.md` 1번부터.
- 성격: 사후 지표. 이 알림이 떴다는 건 사용자가 이미 느끼고 있다는 뜻이다.

## BookingErrorRateHigh

- 조건: `/book` 비 200 응답 비율 > 5%, 1분 지속
- 식: `sum(rate(http_requests_total{route="/book",status!="200"}[2m])) / sum(rate(http_requests_total{route="/book"}[2m])) > 0.05`
- 임계값 근거: 평시 실패율은 0.1% 미만. 5%는 "우연"으로 설명이 안 되는 수준으로 잡았다.
- 첫 대응: 상태코드 분포부터 본다. 500(우리 쪽)인지 502(외부 연동)인지에 따라
  파야 할 곳이 완전히 다르다.

## DBPoolWaitersSustained

- 조건: `avg_over_time(db_pool_waiters[1m]) > 1`, 1분 지속
- 식: `avg_over_time(db_pool_waiters[1m]) > 1`
- 임계값 근거: 평시 이 값은 0이다. 0이 아닌 상태가 지속되는 것 자체가 이상.
- 첫 대응: `runbooks/db-connection-pool.md`의 판정 기준 확인.
- 성격: 선행 신호. 3/14 장애 회고에서 "지연보다 먼저 움직이는 지표"로 신설했다.

## 공통 원칙

- 알림은 위로 튀는 것만 잡지 않는다. 트래픽·성공 수가 평소 대비 **꺼져도** 이상이다.
  (수집 자체가 멈췄을 가능성 포함. 현재 이 방향 알림은 미비 — 개선 백로그.)
- 알림 없이 조용한 장애도 존재한다. 알림 목록은 "이미 얻어맞아 본 것"의 목록일 뿐이다.

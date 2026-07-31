# 런북: DB 커넥션 풀 조정

- 대상 알림: `DBPoolWaitersSustained` — `avg_over_time(db_pool_waiters[1m]) > 1`, 1분 지속
- 최종 수정: 2026-03-21, 김한결
- 현재 운영값: `POOL_SIZE=10` (2026-03-20 상향 적용)

## 풀 고갈 판정 기준

아래 두 개가 **동시에** 보여야 풀 고갈이다. 하나만 보고 판단하지 않는다.

1. `db_pool_connections_in_use`가 풀 크기에 붙어서 평평함
2. `db_pool_waiters`가 0보다 큰 값으로 지속

## 조정 절차

1. `docker-compose.yml`의 `app.environment.POOL_SIZE` 수정
2. `docker compose up -d --build app`
3. 적용 확인 후 10분간 아래를 관찰:
   - `db_pool_waiters` 가 0 부근으로 내려오는가
   - DB 쪽 부담이 늘지 않는가 (커넥션 수, DB 로그)

## 주의 (트레이드오프)

- 풀을 키우면 앱의 대기는 줄지만 **DB의 동시 작업 부담이 늘어난다.**
  풀 크기 합계가 DB `max_connections`에 근접하면 안 된다.
- 풀 확대는 증상 완화다. 유입 자체가 처리 설계를 넘는 상황(티켓 오픈)이면
  대기열/유입 제어 없이 풀만 키우는 건 병목을 DB로 옮기는 것에 가깝다.

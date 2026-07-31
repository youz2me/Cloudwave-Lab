# 티켓 예매 서비스 아키텍처

최종 수정: 2025-11-08, 서태오

## 개요

공연 티켓 예매 서비스. 평소에는 좌석 둘러보기(`/browse`) 트래픽이 대부분이고,
티켓 오픈 순간 예매(`/book`)가 몰리는 스파이크형 트래픽 패턴을 가진다.

## 구성 요소

| 구성 요소 | 설명 |
|-----------|------|
| 앱 서버 | FastAPI. 로드밸런서 뒤에 3대 운영 |
| DB | PostgreSQL 16. 좌석 확정(`reserve_seat()`)과 예매 번호 발급 담당 |
| 캐시 | Redis. 좌석 조회 캐싱 (2025 Q4 도입 완료) |
| 결제 | 외부 PG사 '페이게이트' 연동. 예매 확정 직후 호출 |
| 관측 | Prometheus(:9090) 수집, Grafana(:3000) 조회 |

## 주요 API

- `GET /browse` — 좌석 조회. DB 미사용(캐시 처리)
- `GET /book` — 예매. DB 커넥션 풀 경유, 좌석 확정 쿼리 실행
- `GET /healthz` — 헬스체크
- `GET /metrics` — Prometheus 수집 엔드포인트

## 관측 지표

앱이 내보내는 커스텀 지표:

- `http_requests_total{route,status}` — 경로·상태코드별 요청 수
- `http_request_duration_seconds{route}` — 처리 시간 히스토그램
- `db_pool_connections_in_use` — 사용 중 DB 커넥션 수
- `db_pool_waiters` — 커넥션 대기 중인 요청 수
- `bookings_total{result}` — 예매 성공/실패 수

## 결제 흐름

예매 번호 발급 후 PG사 결제 API를 호출한다. PG 응답 타임아웃 기본값은 3초.
PG 장애 시 예매는 성공했는데 결제만 실패하는 상태가 될 수 있다.

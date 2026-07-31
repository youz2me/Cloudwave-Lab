-- 예매 번호를 발급하는 시퀀스(경합 없는 카운터).
CREATE SEQUENCE IF NOT EXISTS booking_seq;

-- 한 건의 예매를 흉내낸다.
-- pg_sleep(0.05): 좌석 확정에 걸리는 시간 ~50ms를 흉내낸 것.
--   이 동안 이 요청은 DB 커넥션 하나를 계속 붙잡고 있다.
CREATE OR REPLACE FUNCTION reserve_seat() RETURNS BIGINT AS $$
BEGIN
    PERFORM pg_sleep(0.05);
    RETURN nextval('booking_seq');
END;
$$ LANGUAGE plpgsql;

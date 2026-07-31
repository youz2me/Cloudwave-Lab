import asyncio
import os
import random
import time

import asyncpg
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Gauge, Histogram, make_asgi_app

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://booking:booking@db:5432/booking")
POOL_SIZE = int(os.getenv("POOL_SIZE", "5"))

app = FastAPI(title="ticket-booking")

# --- 관측 지표 (Prometheus) ---------------------------------------------------
REQS = Counter("http_requests_total", "HTTP 요청 수", ["route", "status"])
LAT = Histogram(
    "http_request_duration_seconds",
    "요청 처리 시간(초)",
    ["route"],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0, 2.0, 5.0),
)
POOL_INUSE = Gauge("db_pool_connections_in_use", "현재 사용 중인 DB 커넥션 수")
POOL_WAITERS = Gauge("db_pool_waiters", "DB 커넥션을 기다리는 요청 수")
BOOKINGS = Counter("bookings_total", "예매 시도 수", ["result"])

pool: asyncpg.Pool | None = None

# --- 장애 주입 ----------------------------------------------------------------
# 시나리오 스크립트가 켜고 끄는 스위치다. 각 id가 무슨 짓을 하는지는
# 코드를 읽으면 나오지만, 그건 스포일러다. 먼저 관측으로 알아내라.
_FAULT_IDS = {"f1", "f2", "f3"}
_fault: str | None = None


@app.on_event("startup")
async def startup() -> None:
    global pool
    last_err: Exception | None = None
    for _ in range(30):
        try:
            pool = await asyncpg.create_pool(
                DATABASE_URL, min_size=POOL_SIZE, max_size=POOL_SIZE
            )
            return
        except Exception as e:  # DB가 아직 안 떴을 수 있으니 재시도
            last_err = e
            await asyncio.sleep(2)
    raise RuntimeError(f"DB 연결 실패: {last_err}")


@app.on_event("shutdown")
async def shutdown() -> None:
    if pool is not None:
        await pool.close()


async def reserve() -> int:
    POOL_WAITERS.inc()
    try:
        conn = await pool.acquire()
    finally:
        POOL_WAITERS.dec()

    POOL_INUSE.inc()
    try:
        row = await conn.fetchval("SELECT reserve_seat()")
        if _fault == "f1":
            await conn.execute("SELECT pg_sleep(0.95)")
        return int(row)
    finally:
        POOL_INUSE.dec()
        await pool.release(conn)


@app.get("/book")
async def book():
    route, status = "/book", "200"
    start = time.perf_counter()
    try:
        booking_no = await reserve()
        if _fault == "f2" and random.random() < 0.35:
            status = "502"
            BOOKINGS.labels(result="fail").inc()
            return JSONResponse(
                status_code=502, content={"error": "payment gateway timeout"}
            )
        if _fault == "f3":
            booking_no = 4242
        BOOKINGS.labels(result="success").inc()
        return {"booking_no": booking_no}
    except Exception as e:
        status = "500"
        BOOKINGS.labels(result="fail").inc()
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        LAT.labels(route).observe(time.perf_counter() - start)
        REQS.labels(route, status).inc()


@app.get("/browse")
async def browse():
    route, status = "/browse", "200"
    start = time.perf_counter()
    try:
        return {"items": ["A열 12석", "B열 3석", "C열 매진"]}
    finally:
        LAT.labels(route).observe(time.perf_counter() - start)
        REQS.labels(route, status).inc()


@app.get("/healthz")
async def healthz():
    ok = pool is not None
    return JSONResponse(status_code=200 if ok else 503, content={"ok": ok})


@app.post("/admin/fault/{fid}")
async def set_fault(fid: str):
    global _fault
    if fid not in _FAULT_IDS:
        return JSONResponse(status_code=404, content={"error": "unknown fault id"})
    _fault = fid
    return {"fault": fid, "active": True}


@app.delete("/admin/fault")
async def clear_fault():
    global _fault
    _fault = None
    return {"fault": None}


@app.get("/admin/fault")
async def get_fault():
    return {"fault": _fault}


app.mount("/metrics", make_asgi_app())

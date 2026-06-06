from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA = [
    {"region":"apac","latency_ms":175.92,"uptime_pct":98.655},
    {"region":"apac","latency_ms":209.06,"uptime_pct":98.279},
    {"region":"apac","latency_ms":215.56,"uptime_pct":97.265},
    {"region":"apac","latency_ms":158.50,"uptime_pct":97.452},
    {"region":"apac","latency_ms":204.53,"uptime_pct":98.643},
    {"region":"apac","latency_ms":134.75,"uptime_pct":98.895},
    {"region":"apac","latency_ms":149.08,"uptime_pct":98.734},
    {"region":"apac","latency_ms":215.48,"uptime_pct":98.491},
    {"region":"apac","latency_ms":128.81,"uptime_pct":97.424},
    {"region":"apac","latency_ms":157.08,"uptime_pct":99.130},
    {"region":"apac","latency_ms":196.99,"uptime_pct":97.415},
    {"region":"apac","latency_ms":222.13,"uptime_pct":99.034},

    {"region":"emea","latency_ms":203.27,"uptime_pct":97.228},
    {"region":"emea","latency_ms":175.21,"uptime_pct":97.340},
    {"region":"emea","latency_ms":158.90,"uptime_pct":97.190},
    {"region":"emea","latency_ms":152.03,"uptime_pct":97.239},
    {"region":"emea","latency_ms":125.80,"uptime_pct":98.824},
    {"region":"emea","latency_ms":213.53,"uptime_pct":97.844},
    {"region":"emea","latency_ms":171.56,"uptime_pct":99.113},
    {"region":"emea","latency_ms":120.08,"uptime_pct":97.954},
    {"region":"emea","latency_ms":167.46,"uptime_pct":97.670},
    {"region":"emea","latency_ms":132.00,"uptime_pct":98.872},
    {"region":"emea","latency_ms":197.11,"uptime_pct":97.543},
    {"region":"emea","latency_ms":162.65,"uptime_pct":99.425},

    {"region":"amer","latency_ms":112.33,"uptime_pct":97.779},
    {"region":"amer","latency_ms":163.93,"uptime_pct":97.427},
    {"region":"amer","latency_ms":120.44,"uptime_pct":98.160},
    {"region":"amer","latency_ms":143.37,"uptime_pct":99.018},
    {"region":"amer","latency_ms":200.43,"uptime_pct":98.465},
    {"region":"amer","latency_ms":131.87,"uptime_pct":99.440},
    {"region":"amer","latency_ms":206.16,"uptime_pct":97.380},
    {"region":"amer","latency_ms":190.94,"uptime_pct":97.740},
    {"region":"amer","latency_ms":171.67,"uptime_pct":97.996},
    {"region":"amer","latency_ms":223.14,"uptime_pct":97.281},
    {"region":"amer","latency_ms":183.90,"uptime_pct":99.340},
    {"region":"amer","latency_ms":165.39,"uptime_pct":97.819},
]

def p95(values):
    values = sorted(values)
    idx = math.ceil(0.95 * len(values)) - 1
    return values[idx]

@app.post("/api/latency")
async def latency(body: dict):
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)

    result = {}

    for region in regions:
        rows = [r for r in DATA if r["region"] == region]

        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime_pct"] for r in rows]

        result[region] = {
            "avg_latency": round(sum(latencies) / len(latencies), 2),
            "p95_latency": round(p95(latencies), 2),
            "avg_uptime": round(sum(uptimes) / len(uptimes), 3),
            "breaches": sum(1 for x in latencies if x > threshold)
        }

    return result

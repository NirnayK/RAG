import os

import psutil
from fastapi import APIRouter

from core.config import settings

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/system")
async def get_system_metrics():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = {
        part.mountpoint: {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent,
        }
        for part in psutil.disk_partitions()
        for usage in [psutil.disk_usage(part.mountpoint)]
    }
    load = os.getloadavg() if settings.ENABLE_LOADAVG else ()

    return {
        "cpu_percent": cpu,
        "memory": {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "free": mem.free,
            "percent": mem.percent,
        },
        "disk": disk,
        "load_average": {"1m": load[0], "5m": load[1], "15m": load[2]} if load else {},
    }

"""Version 1 API."""

from fastapi import APIRouter

from . import ping, session


router = APIRouter(prefix="/v1")


for i in [
    ping.router,
    session.router,
]:
    router.include_router(i)

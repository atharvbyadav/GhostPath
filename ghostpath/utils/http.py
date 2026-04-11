"""HTTP client helpers."""

from __future__ import annotations

from contextlib import asynccontextmanager

import aiohttp


@asynccontextmanager
async def create_session(timeout: int, user_agent: str):
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    headers = {"User-Agent": user_agent}
    async with aiohttp.ClientSession(timeout=client_timeout, headers=headers) as session:
        yield session

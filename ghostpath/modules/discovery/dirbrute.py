"""Async directory brute forcing."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

import aiohttp

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.utils.parsing import ensure_url


def arg_parser() -> argparse.ArgumentParser:
    parser = build_standard_parser("dirbrute", "Brute force directories with async HTTP requests")
    parser.add_argument("--wordlist", help="Path to wordlist file")
    return parser


def _wordlist_path(custom: str | None) -> Path:
    if custom:
        return Path(custom)
    return Path(__file__).resolve().parents[2] / "data" / "wordlists" / "dirs.txt"


def _load_wordlist(custom: str | None) -> list[str]:
    with _wordlist_path(custom).open("r", encoding="utf-8") as handle:
        return [line.strip().lstrip("/") for line in handle if line.strip()]


async def run(target: str, config: dict | None = None) -> dict:
    config = config or {}
    target = ensure_url(target)
    timeout = int(config.get("timeout", 10))
    limit = int(config.get("threads", 20))
    user_agent = str(config.get("user_agent", "GhostPath/3.0"))
    words = _load_wordlist(config.get("wordlist"))
    semaphore = asyncio.Semaphore(limit)
    connector = aiohttp.TCPConnector(limit=limit)
    client_timeout = aiohttp.ClientTimeout(total=timeout)

    async def probe(path: str) -> str | None:
        url = f"{target.rstrip('/')}/{path}"
        async with semaphore:
            try:
                async with session.get(url, allow_redirects=False) as response:
                    if response.status in {200, 204, 301, 302, 403}:
                        return f"{url} [{response.status}]"
            except aiohttp.ClientError:
                return None
        return None

    async with aiohttp.ClientSession(
        timeout=client_timeout,
        headers={"User-Agent": user_agent},
        connector=connector,
    ) as session:
        results = await asyncio.gather(*[probe(word) for word in words])

    hits = sorted(item for item in results if item)
    return default_result("dirbrute", hits, {"count": len(hits), "attempted": len(words)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("dirbrute", run, args)

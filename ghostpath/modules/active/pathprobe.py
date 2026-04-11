"""Async path probing module."""

from __future__ import annotations

import argparse
from pathlib import Path

import aiohttp

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.utils.parsing import ensure_url


def arg_parser() -> argparse.ArgumentParser:
    parser = build_standard_parser("pathprobe", "Actively probe endpoints on a target domain")
    parser.add_argument("--wordlist", help="Path to custom wordlist file")
    return parser


def _default_wordlist() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "path-wordlist.txt"


def _load_wordlist(path: str | None) -> list[str]:
    wordlist_path = Path(path) if path else _default_wordlist()
    with wordlist_path.open("r", encoding="utf-8") as handle:
        return [line.strip().lstrip("/") for line in handle if line.strip()]


async def _probe_path(session: aiohttp.ClientSession, semaphore, target: str, path: str) -> str | None:
    url = f"{target.rstrip('/')}/{path}"
    async with semaphore:
        try:
            async with session.get(url, allow_redirects=False) as response:
                if response.status in {200, 204, 301, 302, 403}:
                    return f"{url} [{response.status}]"
        except aiohttp.ClientError:
            return None
    return None


async def run(target: str, config: dict | None = None) -> dict:
    config = config or {}
    target = ensure_url(target)
    timeout = int(config.get("timeout", 10))
    threads = int(config.get("threads", 20))
    user_agent = str(config.get("user_agent", "GhostPath/3.0"))
    wordlist = _load_wordlist(config.get("wordlist"))
    connector = aiohttp.TCPConnector(limit=threads)
    semaphore = __import__("asyncio").Semaphore(threads)
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(
        timeout=client_timeout,
        headers={"User-Agent": user_agent},
        connector=connector,
    ) as session:
        tasks = [_probe_path(session, semaphore, target, path) for path in wordlist]
        responses = await __import__("asyncio").gather(*tasks)
    results = sorted([item for item in responses if item])
    return default_result("pathprobe", results, {"count": len(results), "attempted": len(wordlist)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("pathprobe", run, args)

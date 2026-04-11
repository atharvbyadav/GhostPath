"""Historical URL discovery."""

from __future__ import annotations

import argparse
from urllib.parse import urlparse

import requests

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.utils.parsing import extract_domain


def arg_parser() -> argparse.ArgumentParser:
    parser = build_standard_parser("timetrail", "Fetch historical URLs from Wayback, URLScan, and Common Crawl")
    parser.add_argument(
        "--source",
        choices=["wayback", "urlscan", "commoncrawl", "all"],
        default="commoncrawl",
        help="Archive source",
    )
    return parser


def fetch_wayback_urls(domain: str, timeout: int, user_agent: str) -> list[str]:
    response = requests.get(
        "https://web.archive.org/cdx/search/cdx",
        params={"url": f"*.{domain}/*", "output": "text", "fl": "original", "collapse": "urlkey", "limit": 5000},
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )
    response.raise_for_status()
    return sorted({line.strip() for line in response.text.splitlines() if line.strip()})


def fetch_urlscan_urls(domain: str, timeout: int, user_agent: str) -> list[str]:
    response = requests.get(
        "https://urlscan.io/api/v1/search/",
        params={"q": f"domain:{domain}", "size": 1000},
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )
    response.raise_for_status()
    urls = {
        item.get("page", {}).get("url", "").strip()
        for item in response.json().get("results", [])
        if item.get("page", {}).get("url")
    }
    return sorted(_filter_by_domain(urls, domain))


def fetch_commoncrawl_urls(domain: str, timeout: int, user_agent: str) -> list[str]:
    response = requests.get(
        f"https://index.commoncrawl.org/CC-MAIN-2024-10-index?url=*.{domain}/*&output=json",
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )
    response.raise_for_status()
    urls = []
    for line in response.text.splitlines():
        if '"url"' not in line:
            continue
        parts = line.split('"url":"')
        if len(parts) > 1:
            urls.append(parts[1].split('"', maxsplit=1)[0].replace("\\/", "/"))
    return sorted(set(urls))


def _filter_by_domain(urls: set[str], domain: str) -> list[str]:
    filtered = []
    for url in urls:
        host = urlparse(url).hostname
        if host and (host == domain or host.endswith(f".{domain}")):
            filtered.append(url)
    return filtered


def run(target: str, config: dict | None = None) -> dict:
    config = config or {}
    target = extract_domain(target)
    source = config.get("source", "commoncrawl")
    timeout = int(config.get("timeout", 10))
    user_agent = str(config.get("user_agent", "GhostPath/3.0"))

    urls: set[str] = set()
    if source in {"wayback", "all"}:
        urls.update(fetch_wayback_urls(target, timeout, user_agent))
    if source in {"urlscan", "all"}:
        urls.update(fetch_urlscan_urls(target, timeout, user_agent))
    if source in {"commoncrawl", "all"}:
        urls.update(fetch_commoncrawl_urls(target, timeout, user_agent))

    return default_result("timetrail", sorted(urls), {"source": source, "count": len(urls)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("timetrail", run, args)

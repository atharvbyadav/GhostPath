"""Passive-forward domain discovery."""

from __future__ import annotations

import argparse
import re

import requests

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.utils.parsing import extract_domain


def arg_parser() -> argparse.ArgumentParser:
    return build_standard_parser("domainscope", "Enumerate subdomains from crt.sh and URLScan")


def _fetch_crtsh(domain: str, timeout: int, user_agent: str) -> set[str]:
    response = requests.get(
        f"https://crt.sh/?q=%25.{domain}&output=json",
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )
    response.raise_for_status()
    values = set()
    for cert in response.json():
        for subdomain in cert.get("name_value", "").splitlines():
            values.add(subdomain.strip().lstrip("*."))
    return values


def _fetch_urlscan(domain: str, timeout: int, user_agent: str) -> set[str]:
    response = requests.get(
        "https://urlscan.io/api/v1/search/",
        params={"q": f"domain:{domain}", "size": 1000},
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )
    response.raise_for_status()
    return {
        result.get("page", {}).get("domain", "").strip()
        for result in response.json().get("results", [])
        if result.get("page", {}).get("domain")
    }


def run(target: str, config: dict | None = None) -> dict:
    config = config or {}
    target = extract_domain(target)
    timeout = int(config.get("timeout", 10))
    user_agent = str(config.get("user_agent", "GhostPath/3.0"))
    regex = re.compile(rf"^(?:[\w-]+\.)*{re.escape(target)}$", re.IGNORECASE)
    found = _fetch_crtsh(target, timeout, user_agent) | _fetch_urlscan(target, timeout, user_agent)
    valid = sorted({item for item in found if regex.match(item)})
    return default_result("domainscope", valid, {"count": len(valid)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("domainscope", run, args)

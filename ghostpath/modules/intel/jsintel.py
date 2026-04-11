"""JavaScript intelligence extraction."""

from __future__ import annotations

import argparse
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.utils.parsing import ENDPOINT_REGEX, SECRET_REGEX, ensure_url


def arg_parser() -> argparse.ArgumentParser:
    return build_standard_parser("jsintel", "Extract endpoints, keys, tokens, and domains from JavaScript")


def run(target: str, config: dict | None = None) -> dict:
    config = config or {}
    timeout = int(config.get("timeout", 10))
    user_agent = str(config.get("user_agent", "GhostPath/3.0"))
    response = requests.get(ensure_url(target), headers={"User-Agent": user_agent}, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    findings = set()
    for script in soup.find_all("script", src=True):
        src = urljoin(response.url, script["src"])
        js_response = requests.get(src, headers={"User-Agent": user_agent}, timeout=timeout)
        if not js_response.ok:
            continue
        body = js_response.text
        findings.update(ENDPOINT_REGEX.findall(body))
        findings.update(match for match in SECRET_REGEX.findall(body) if match)
        findings.update(
            token
            for token in body.split()
            if "." in token and any(suffix in token.lower() for suffix in [".internal", ".local", ".corp"])
        )

    return default_result("jsintel", sorted(findings), {"count": len(findings)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("jsintel", run, args)

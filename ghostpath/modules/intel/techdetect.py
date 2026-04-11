"""Technology detection using headers and HTML patterns."""

from __future__ import annotations

import argparse

import requests
from bs4 import BeautifulSoup

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.utils.parsing import ensure_url


PATTERNS = {
    "wordpress": "wp-content",
    "drupal": "/sites/default/",
    "nginx": "nginx",
    "apache": "apache",
    "cloudflare": "cloudflare",
    "react": "react",
    "vue": "vue",
}


def arg_parser() -> argparse.ArgumentParser:
    return build_standard_parser("techdetect", "Detect server, framework, CMS, and CDN indicators")


def run(target: str, config: dict | None = None) -> dict:
    config = config or {}
    timeout = int(config.get("timeout", 10))
    user_agent = str(config.get("user_agent", "GhostPath/3.0"))
    response = requests.get(ensure_url(target), headers={"User-Agent": user_agent}, timeout=timeout)
    response.raise_for_status()
    html = response.text.lower()
    headers = {key.lower(): value.lower() for key, value in response.headers.items()}
    soup = BeautifulSoup(response.text, "html.parser")

    findings = set()
    for name, marker in PATTERNS.items():
        if marker in html or any(marker in value for value in headers.values()):
            findings.add(name)
    server = headers.get("server")
    if server:
        findings.add(f"server:{server}")
    powered_by = headers.get("x-powered-by")
    if powered_by:
        findings.add(f"framework:{powered_by}")
    for meta in soup.find_all("meta"):
        generator = meta.attrs.get("name", "").lower()
        if generator == "generator":
            findings.add(f"cms:{meta.attrs.get('content', '')}")

    return default_result("techdetect", sorted(findings), {"count": len(findings)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("techdetect", run, args)

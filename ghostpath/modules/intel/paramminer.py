"""Parameter mining from archives, JS, and forms."""

from __future__ import annotations

import argparse
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.modules.passive.timetrail import fetch_wayback_urls
from ghostpath.utils.parsing import PARAMETER_REGEX, ensure_url, extract_domain


def arg_parser() -> argparse.ArgumentParser:
    return build_standard_parser("paramminer", "Extract interesting parameters from archives, JS, and forms")


def _extract_from_urls(urls: list[str]) -> set[str]:
    params = set()
    for url in urls:
        params.update(PARAMETER_REGEX.findall(url))
    return params


def _extract_forms(target: str, timeout: int, user_agent: str) -> set[str]:
    response = requests.get(ensure_url(target), headers={"User-Agent": user_agent}, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    params = set()
    for form in soup.find_all("form"):
        for field in form.find_all(["input", "textarea", "select"]):
            name = field.get("name")
            if name:
                params.add(name)
    return params


def _extract_js_params(target: str, timeout: int, user_agent: str) -> set[str]:
    response = requests.get(ensure_url(target), headers={"User-Agent": user_agent}, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    params = set()
    for script in soup.find_all("script", src=True):
        src = urljoin(response.url, script["src"])
        js_response = requests.get(src, headers={"User-Agent": user_agent}, timeout=timeout)
        if js_response.ok:
            params.update(PARAMETER_REGEX.findall(js_response.text))
    return params


def run(target: str, config: dict | None = None) -> dict:
    config = config or {}
    timeout = int(config.get("timeout", 10))
    user_agent = str(config.get("user_agent", "GhostPath/3.0"))
    archive_urls = fetch_wayback_urls(extract_domain(target), timeout, user_agent)
    params = set()
    params.update(_extract_from_urls(archive_urls))
    params.update(_extract_forms(target, timeout, user_agent))
    params.update(_extract_js_params(target, timeout, user_agent))
    interesting = sorted(
        {
            param
            for param in params
            if param.lower() in {"id", "token", "redirect", "url", "next"} or param
        }
    )
    return default_result("paramminer", interesting, {"count": len(interesting)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("paramminer", run, args)

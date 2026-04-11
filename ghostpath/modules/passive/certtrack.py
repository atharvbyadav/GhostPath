"""Certificate transparency module."""

from __future__ import annotations

import argparse
import re

import requests

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.utils.parsing import extract_domain


def arg_parser() -> argparse.ArgumentParser:
    return build_standard_parser("certtrack", "Discover subdomains via crt.sh certificate transparency logs")


def run(target: str, config: dict | None = None) -> dict:
    config = config or {}
    target = extract_domain(target)
    timeout = int(config.get("timeout", 10))
    user_agent = str(config.get("user_agent", "GhostPath/3.0"))
    response = requests.get(
        f"https://crt.sh/?q=%25.{target}&output=json",
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )
    response.raise_for_status()
    subdomains = set()
    for entry in response.json():
        for name in entry.get("name_value", "").splitlines():
            if name.strip():
                subdomains.add(name.strip().lstrip("*."))

    regex = re.compile(rf"^(?:[\w-]+\.)*{re.escape(target)}$", re.IGNORECASE)
    valid = sorted({item for item in subdomains if regex.match(item)})
    return default_result("certtrack", valid, {"count": len(valid)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("certtrack", run, args)

"""Subdomain permutation engine."""

from __future__ import annotations

import argparse

from ghostpath.modules.base import build_standard_parser, cli_entry, default_result
from ghostpath.utils.parsing import extract_domain


PREFIXES = ["dev", "test", "staging", "beta", "internal", "api", "cdn", "static"]


def arg_parser() -> argparse.ArgumentParser:
    return build_standard_parser("sub_permuter", "Generate probable subdomains")


def run(target: str, config: dict | None = None) -> dict:
    target = extract_domain(target)
    permutations = sorted({f"{prefix}.{target}" for prefix in PREFIXES})
    return default_result("sub_permuter", permutations, {"count": len(permutations)})


def cli(args: argparse.Namespace) -> dict:
    return cli_entry("sub_permuter", run, args)

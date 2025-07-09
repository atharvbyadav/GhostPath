import requests
import json
import argparse
import re
from ghostpath.modules.shared import logger, output

def arg_parser():
    parser = argparse.ArgumentParser(
        prog="certtrack",
        description="Discover subdomains via Certificate Transparency logs (crt.sh)"
    )
    parser.add_argument("--target", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("--output", help="Path to save results")
    parser.add_argument("--format", choices=["json", "txt", "csv"], default="txt", help="Output format (default: txt)")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug output")
    return parser

def run(args):
    if args.debug:
        logger.enable_debug()

    domain = args.target
    logger.debug(f"Querying crt.sh for Certificate Transparency data on: {domain}")

    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        headers = {"User-Agent": "GhostPath-CertTrack/2025"}

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        subdomains = set()
        for entry in data:
            name_val = entry.get("name_value", "")
            for name in name_val.split("\n"):
                name = name.strip()
                if domain in name:
                    subdomains.add(name)

        logger.debug(f"Fetched {len(subdomains)} raw entries from crt.sh")

        valid, noisy = filter_valid_subdomains(subdomains, domain)
        logger.debug(f"Filtered: {len(valid)} valid, {len(noisy)} noisy")

        if not valid and not noisy:
            print("[!] No results found.")
            return

        if args.output:
            output.save_results(valid, args.output, args.format)
            print(f"[CertTrack] Results saved to: {args.output}")
        else:
            for sub in sorted(valid):
                print(sub)

        if noisy:
            print("\n⚠️  Some extra entries were found but skipped from main list:")
            for n in sorted(noisy):
                print(f"  - {n}")

    except Exception as e:
        logger.debug(f"CertTrack error: {e}")
        print(f"[CertTrack] Error: {e}")

def filter_valid_subdomains(entries, domain):
    valid = set()
    noisy = set()

    domain_regex = re.compile(rf"^(?:[\w-]+\.)*{re.escape(domain)}$", re.IGNORECASE)

    for entry in entries:
        e = entry.strip()
        if " " in e or "@" in e:
            noisy.add(e)
        elif domain_regex.match(e):
            valid.add(e)
        else:
            noisy.add(e)

    return list(valid), list(noisy)

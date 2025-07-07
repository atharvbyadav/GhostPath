# ghostpath/modules/certtrack.py

import requests
import json
from modules.shared import logger, output
import argparse

def arg_parser():
    parser = argparse.ArgumentParser(
        prog="certtrack",
        description="Discover subdomains via Certificate Transparency logs (crt.sh)"
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target domain (e.g., example.com)"
    )
    parser.add_argument(
        "--output",
        help="Path to save results"
    )
    parser.add_argument(
        "--format",
        choices=["json", "txt", "csv"],
        default="txt",
        help="Output format (default: txt)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose debug output"
    )
    return parser

def run(args):
    if args.debug:
        logger.enable_debug()

    domain = args.target
    logger.debug(f"Querying crt.sh for Certificate Transparency data on: {domain}")

    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        headers = {
            "User-Agent": "GhostPath-CertTrack/2025"
        }

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

        logger.debug(f"Retrieved {len(subdomains)} unique subdomains from crt.sh")

        if args.output:
            output.save_results(list(subdomains), args.output, args.format)
            print(f"[CertTrack] Results saved to: {args.output}")
        else:
            for sub in sorted(subdomains):
                print(sub)

    except Exception as e:
        print(f"[CertTrack] Error: {e}")

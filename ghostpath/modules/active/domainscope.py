# ghostpath/modules/domainscope.py

import requests
import json
from modules.shared import logger, output
import argparse

def arg_parser():
    parser = argparse.ArgumentParser(
        prog="domainscope",
        description="Enumerate subdomains from passive DNS sources like crt.sh and URLScan"
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target domain to enumerate subdomains for (e.g., example.com)"
    )
    parser.add_argument(
        "--output",
        help="Path to save output file"
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
    logger.debug(f"Enumerating subdomains for domain: {domain}")

    try:
        crtsh_subdomains = fetch_crtsh(domain)
        urlscan_subdomains = fetch_urlscan(domain)

        all_subdomains = set(crtsh_subdomains + urlscan_subdomains)
        logger.debug(f"Total unique subdomains discovered: {len(all_subdomains)}")

        if args.output:
            output.save_results(all_subdomains, args.output, args.format)
            print(f"[DomainScope] Results saved to: {args.output}")
        else:
            for sub in sorted(all_subdomains):
                print(sub)

    except Exception as e:
        print(f"[DomainScope] Error: {e}")

def fetch_crtsh(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {"User-Agent": "GhostPath-DomainScope"}

    logger.debug(f"Querying crt.sh for: {domain}")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        subdomains = set()
        for cert in data:
            name_value = cert.get("name_value", "")
            for sub in name_value.split("\n"):
                if domain in sub:
                    subdomains.add(sub.strip())

        logger.debug(f"Found {len(subdomains)} subdomains from crt.sh")
        return list(subdomains)

    except Exception as e:
        logger.debug(f"crt.sh fetch failed: {e}")
        return []

def fetch_urlscan(domain):
    url = "https://urlscan.io/api/v1/search/"
    params = {"q": f"domain:{domain}", "size": 1000}
    headers = {"User-Agent": "GhostPath-DomainScope"}

    logger.debug(f"Querying URLScan for: {domain}")
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        subdomains = set()
        for entry in data.get("results", []):
            page_url = entry.get("page", {}).get("domain", "")
            if page_url and domain in page_url:
                subdomains.add(page_url.strip())

        logger.debug(f"Found {len(subdomains)} subdomains from URLScan")
        return list(subdomains)

    except Exception as e:
        logger.debug(f"URLScan fetch failed: {e}")
        return []

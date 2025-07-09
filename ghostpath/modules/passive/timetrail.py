import requests
import time
import json
from urllib.parse import urlparse
from ghostpath.modules.shared import output, logger
import argparse

def arg_parser():
    parser = argparse.ArgumentParser(
        prog="timetrail",
        description="Fetch historical URLs from archives like Wayback Machine, URLScan, and Common Crawl"
    )
    parser.add_argument("--target", required=True, help="Target domain for historical URL discovery (e.g., example.com)")
    parser.add_argument("--source", choices=["wayback", "urlscan", "commoncrawl"], default="commoncrawl", help="Archive source: wayback | urlscan | commoncrawl (default: commoncrawl)")
    parser.add_argument("--output", help="Path to save output file")
    parser.add_argument("--format", choices=["json", "txt", "csv"], default="txt", help="Output format (default: txt)")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug output")
    return parser

def run(args):
    if args.debug:
        logger.enable_debug()

    domain = args.target
    logger.debug(f"Fetching historical URLs for domain: {domain} from source: {args.source}")

    try:
        if args.source == "wayback":
            urls = fetch_wayback_urls(domain)
        elif args.source == "urlscan":
            urls = fetch_urlscan_urls(domain)
        elif args.source == "commoncrawl":
            urls = fetch_commoncrawl_urls(domain)
        else:
            raise ValueError(f"Unsupported source: {args.source}")

        logger.debug(f"Total unique URLs fetched: {len(urls)}")

        if not urls:
            print("[!] No results found.")
            return

        filename = args.output
        if not filename:
            filename = f"{args.target}.{args.format}"

        output.save_results(urls, filename, args.format)
        print(f"[TimeTrail] Results saved to: {filename}")

    except Exception as e:
        logger.debug(f"TimeTrail error: {e}")
        print(f"[TimeTrail] Error: {e}")

def fetch_wayback_urls(domain, retries=3):
    url = "https://web.archive.org/cdx/search/cdx"
    params = {
        "url": f"*.{domain}/*",
        "output": "text",
        "fl": "original",
        "collapse": "urlkey",
        "limit": 5000
    }
    headers = {"User-Agent": "Mozilla/5.0 (GhostPath/2025)"}

    logger.debug(f"Wayback API URL: {url} with params {params}")

    attempt = 0
    while attempt < retries:
        try:
            logger.debug(f"Attempt {attempt + 1} - Sending request...")

            with requests.get(url, headers=headers, params=params, timeout=60, stream=True) as response:
                logger.debug(f"HTTP {response.status_code} Response from Wayback")
                response.raise_for_status()

                urls = set(
                    line.strip() for line in response.iter_lines(decode_unicode=True)
                    if line and line.strip()
                )

                logger.debug(f"Retrieved {len(urls)} unique URLs from Wayback.")
                return list(urls)

        except requests.RequestException as e:
            logger.debug(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 * (attempt + 1))

        attempt += 1

    raise Exception(f"Failed to fetch Wayback URLs for {domain} after {retries} attempts")

def fetch_urlscan_urls(domain, retries=3):
    api_url = "https://urlscan.io/api/v1/search/"
    params = {"q": f"domain:{domain}", "size": 1000}
    headers = {"User-Agent": "Mozilla/5.0 (GhostPath/2025)"}

    logger.debug(f"URLScan API URL: {api_url} with params {params}")

    attempt = 0
    all_urls = set()

    while attempt < retries:
        try:
            logger.debug(f"Attempt {attempt + 1} - Sending request to URLScan...")

            response = requests.get(api_url, headers=headers, params=params, timeout=30)
            logger.debug(f"HTTP {response.status_code} Response from URLScan")

            response.raise_for_status()
            data = response.json()

            for result in data.get("results", []):
                url = result.get("page", {}).get("url")
                if url:
                    all_urls.add(url.strip())

            filtered_urls = filter_urls_by_domain(all_urls, domain)
            logger.debug(f"Filtered down to {len(filtered_urls)} URLs after domain check.")
            return filtered_urls

        except requests.RequestException as e:
            logger.debug(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 * (attempt + 1))

        attempt += 1

    raise Exception(f"Failed to fetch URLs from URLScan after {retries} attempts")

def fetch_commoncrawl_urls(domain, retries=3):
    index_url = "https://index.commoncrawl.org/CC-MAIN-2024-10-index"
    query_url = f"{index_url}?url=*.{domain}/*&output=json"
    headers = {"User-Agent": "Mozilla/5.0 (GhostPath/2025)"}

    logger.debug(f"Common Crawl API URL: {query_url}")

    attempt = 0
    urls = set()

    while attempt < retries:
        try:
            logger.debug(f"Attempt {attempt + 1} - Querying Common Crawl...")

            response = requests.get(query_url, headers=headers, timeout=30, stream=True)
            logger.debug(f"HTTP {response.status_code} from Common Crawl")

            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        record = json.loads(line)
                        if 'url' in record:
                            urls.add(record['url'].strip())
                    except Exception as parse_err:
                        logger.debug(f"JSON parse error: {parse_err}")

            logger.debug(f"Retrieved {len(urls)} unique URLs from Common Crawl.")
            return list(urls)

        except requests.RequestException as e:
            logger.debug(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 * (attempt + 1))

        attempt += 1

    raise Exception(f"Failed to fetch URLs from Common Crawl after {retries} attempts")

def filter_urls_by_domain(urls, target_domain):
    filtered = set()
    for url in urls:
        try:
            hostname = urlparse(url).hostname
            if hostname and (hostname == target_domain or hostname.endswith(f".{target_domain}")):
                filtered.add(url)
        except Exception as e:
            logger.debug(f"URL parsing error for {url}: {e}")
    return list(filtered)

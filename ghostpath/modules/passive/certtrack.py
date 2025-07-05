import requests
import time
from modules.shared import output, logger

def add_arguments(parser):
    parser.add_argument(
        "--target",
        required=True,
        help="Target domain for subdomain enumeration (e.g., example.com)"
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

def run(args):
    if args.debug:
        logger.enable_debug()

    domain = args.target
    logger.debug(f"Fetching subdomains for domain: {domain} from crt.sh")

    try:
        subdomains = fetch_crtsh_subdomains(domain)
        logger.debug(f"Total unique subdomains fetched: {len(subdomains)}")

        if args.output:
            output.save_results(subdomains, args.output, args.format)
            print(f"[CertTrack] Results saved to: {args.output}")
        else:
            print("\n".join(subdomains))

    except Exception as e:
        print(f"[CertTrack] Error: {e}")

def fetch_crtsh_subdomains(domain, retries=3):
    url = "https://crt.sh/"
    params = {
        "q": f"%.{domain}",
        "output": "json"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (GhostPath/2025)"
    }

    attempt = 0
    subdomains = set()

    while attempt < retries:
        try:
            logger.debug(f"Attempt {attempt + 1} - Querying crt.sh...")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            logger.debug(f"HTTP {response.status_code} Response from crt.sh")

            response.raise_for_status()
            data = response.json()

            for entry in data:
                name_value = entry.get('name_value', '')
                for sub in name_value.splitlines():
                    if sub.endswith(domain):
                        subdomains.add(sub.strip())

            logger.debug(f"Retrieved {len(subdomains)} unique subdomains from crt.sh.")
            return list(subdomains)

        except requests.RequestException as e:
            logger.debug(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 * (attempt + 1))

        attempt += 1

    raise Exception(f"Failed to fetch subdomains from crt.sh after {retries} attempts")

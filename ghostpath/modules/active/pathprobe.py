import requests
import time
from modules.shared import output, logger

def add_arguments(parser):
    parser.add_argument(
        "--target",
        required=True,
        help="Target URL for directory brute-forcing (e.g., https://example.com)"
    )
    parser.add_argument(
        "--wordlist",
        required=True,
        help="Path to wordlist file (one path per line)"
    )
    parser.add_argument(
        "--status",
        nargs="+",
        type=int,
        default=[200, 301, 302],
        help="HTTP status codes to match (default: 200 301 302)"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Number of concurrent threads (default: 10)"
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

    target_url = args.target.rstrip("/")
    logger.debug(f"Starting PathProbe on target: {target_url}")

    try:
        with open(args.wordlist, "r") as f:
            paths = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[PathProbe] Error reading wordlist: {e}")
        return

    logger.debug(f"Loaded {len(paths)} paths from wordlist.")

    from concurrent.futures import ThreadPoolExecutor

    results = []

    def probe_path(path):
        url = f"{target_url}/{path}"
        retries = 3
        attempt = 0

        while attempt < retries:
            try:
                logger.debug(f"Attempt {attempt + 1} - Probing {url}")
                response = requests.get(url, timeout=10, allow_redirects=False)
                if response.status_code in args.status:
                    logger.debug(f"Found: {url} [{response.status_code}]")
                    return f"{url} [{response.status_code}]"
                break
            except requests.RequestException as e:
                logger.debug(f"Attempt {attempt + 1} failed for {url}: {e}")
                time.sleep(2 * (attempt + 1))
                attempt += 1
        return None

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for result in executor.map(probe_path, paths):
            if result:
                results.append(result)

    logger.debug(f"Total paths found: {len(results)}")

    if args.output:
        output.save_results(results, args.output, args.format)
        print(f"[PathProbe] Results saved to: {args.output}")
    else:
        print("\n".join(results))

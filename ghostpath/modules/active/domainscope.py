import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from modules.shared import output, logger

def add_arguments(parser):
    parser.add_argument(
        "--target",
        required=True,
        help="Target domain for subdomain discovery (e.g., example.com)"
    )
    parser.add_argument(
        "--input-file",
        required=True,
        help="Path to wordlist file containing subdomain prefixes"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=10,
        help="Number of parallel workers (default: 10)"
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

    target_domain = args.target
    wordlist_path = args.input_file
    workers = args.workers

    logger.debug(f"Starting DomainScope on target: {target_domain}")
    logger.debug(f"Using wordlist: {wordlist_path}")
    logger.debug(f"Using {workers} threads")

    try:
        with open(wordlist_path, "r") as f:
            prefixes = [line.strip() for line in f if line.strip()]

        logger.debug(f"Total prefixes loaded: {len(prefixes)}")

        results = []

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_subdomain = {
                executor.submit(resolve_subdomain, prefix, target_domain): prefix for prefix in prefixes
            }

            for future in as_completed(future_to_subdomain):
                prefix = future_to_subdomain[future]
                try:
                    resolved_ip = future.result()
                    if resolved_ip:
                        full_subdomain = f"{prefix}.{target_domain}"
                        results.append({
                            "subdomain": full_subdomain,
                            "ip": resolved_ip
                        })
                        print(f"[FOUND] {full_subdomain} -> {resolved_ip}")
                except Exception as e:
                    logger.debug(f"Error resolving '{prefix}': {e}")

        logger.debug(f"Total live subdomains found: {len(results)}")

        if args.output:
            output.save_results(results, args.output, args.format)
            print(f"[DomainScope] Results saved to: {args.output}")

    except FileNotFoundError:
        print(f"[DomainScope] Error: Wordlist file not found: {wordlist_path}")
    except Exception as e:
        print(f"[DomainScope] Unexpected error: {e}")

def resolve_subdomain(prefix, domain):
    subdomain = f"{prefix}.{domain}"
    logger.debug(f"Resolving subdomain: {subdomain}")
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except socket.gaierror:
        logger.debug(f"Subdomain not found: {subdomain}")
        return None

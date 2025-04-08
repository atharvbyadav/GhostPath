import argparse
from fetchers.wayback import get_wayback_urls
from fetchers.subdomains import get_subdomains_crtsh
from utils.dedup import deduplicate_urls

def main():
    parser = argparse.ArgumentParser(description="GhostPath - Hunt historical URLs like a ghost.")
    parser.add_argument("domain", help="Target domain (e.g. example.com)")
    parser.add_argument("--subs", action="store_true", help="Include subdomains via crt.sh")
    args = parser.parse_args()

    targets = [args.domain]

    if args.subs:
        print(f"[+] Fetching subdomains for {args.domain}...")
        subs = get_subdomains_crtsh(args.domain)
        targets.extend(subs)

    all_urls = set()

    for target in targets:
        print(f"[+] Fetching URLs for {target}...")
        urls = get_wayback_urls(target)
        all_urls.update(urls)

    final_urls = deduplicate_urls(all_urls)

    print(f"\n[+] Found {len(final_urls)} unique URLs:")
    for url in final_urls:
        print(url)

if __name__ == "__main__":
    main()

import requests
import threading
from queue import Queue
from ghostpath.modules.shared import logger, output
import argparse
import os

import importlib.resources as pkg_resources

print_lock = threading.Lock()

def arg_parser():
    parser = argparse.ArgumentParser(
        prog="pathprobe",
        description="Actively probe endpoints/paths on a target domain using multithreaded HTTP checks"
    )
    parser.add_argument("--target", required=True, help="Target domain (e.g., https://example.com)")
    parser.add_argument("--wordlist", help="Path to custom wordlist file (default: ghostpath/data/path-wordlist.txt)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("--output", help="Path to save results")
    parser.add_argument("--format", choices=["json", "txt", "csv"], default="txt", help="Output format")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug output")
    return parser

def run(args):
    if args.debug:
        logger.enable_debug()

    target = args.target.rstrip("/")
    logger.debug(f"Starting path probe on: {target}")

    wordlist = load_wordlist(args.wordlist)
    if not wordlist:
        print("[!] No wordlist found. Provide one using --wordlist or ensure 'path-wordlist.txt' exists in ghostpath/data/")
        return

    found_paths = []
    q = Queue()
    total_attempts = 0
    total_attempts_lock = threading.Lock()

    def worker():
        nonlocal total_attempts
        while not q.empty():
            path = q.get()
            url = f"{target}/{path}"
            try:
                res = requests.get(url, timeout=8)
                with total_attempts_lock:
                    total_attempts += 1
                if res.status_code in [200, 204, 301, 302, 403]:
                    with print_lock:
                        if res.status_code == 200:
                            print(f"\033[92m[+] {url} (200 OK)\033[0m")
                        elif res.status_code in [301, 302]:
                            print(f"\033[93m[→] {url} ({res.status_code} Redirect)\033[0m")
                        elif res.status_code == 403:
                            print(f"\033[91m[×] {url} (403 Forbidden)\033[0m")
                        found_paths.append(f"{url} [{res.status_code}]")
                    logger.debug(f"Found: {url} [{res.status_code}]")
            except requests.RequestException as e:
                logger.debug(f"Request failed for {url}: {e}")
            finally:
                q.task_done()

    for word in wordlist:
        q.put(word)

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    q.join()
    for t in threads:
        t.join()

    if not found_paths:
        print("[!] No valid paths found.")

    print(f"[PathProbe] Attempted {total_attempts} total paths")
    print(f"[PathProbe] Found {len(found_paths)} valid paths")

    if args.output:
        clean_urls = [p.split(" [")[0] for p in found_paths]
        output.save_results(clean_urls, args.output, args.format)
        print(f"[PathProbe] Results saved to: {args.output}")
    else:
        for p in found_paths:
            print(p)

def load_wordlist(path):
    if path and os.path.isfile(path):
        with open(path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            logger.debug(f"Loaded {len(lines)} paths from custom wordlist: {path}")
            return lines

    try:
        with pkg_resources.open_text("ghostpath.data", "path-wordlist.txt") as f:
            lines = [line.strip() for line in f if line.strip()]
            logger.debug("Loaded paths from packaged wordlist in ghostpath/data/path-wordlist.txt")
            return lines
    except FileNotFoundError:
        logger.debug("Failed to find packaged wordlist ghostpath/data/path-wordlist.txt")
        return []

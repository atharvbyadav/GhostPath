import requests

def get_wayback_urls(domain):
    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=text&fl=original&collapse=urlkey"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return set(r.text.strip().splitlines())
        return set()
    except Exception as e:
        print(f"[!] Error fetching Wayback URLs: {e}")
        return set()

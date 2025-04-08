import requests

def get_subdomains_crtsh(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        subdomains = set()
        for entry in data:
            name = entry['name_value']
            if '\n' in name:
                subdomains.update(name.split('\n'))
            else:
                subdomains.add(name)
        return list(subdomains)
    except Exception as e:
        print(f"[!] Error fetching subdomains: {e}")
        return []

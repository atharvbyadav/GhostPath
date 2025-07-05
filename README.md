<h1 align="center">👻 GhostPath — Uncover The Web's Hidden Trails</h1>

<p align="center">
  <img src="https://img.shields.io/badge/license-BSD%203--Clause-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/type-Passive%20%2F%20Active%20Recon-yellow" alt="Recon Type">
  <img src="https://img.shields.io/badge/modules-TimeTrail%20|%20CertTrack%20|%20PathProbe-orange" alt="Modules">
  <img src="https://img.shields.io/badge/focus-OSINT%20Recon-red" alt="Focus">
  <img src="https://img.shields.io/badge/debug-Verbose%20Logs%20Available-lightgrey" alt="Debug">
  <img src="https://img.shields.io/badge/platform-Linux%20|%20WSL%20|%20MacOS-lightgreen" alt="Platform">
  <img src="https://img.shields.io/badge/status-Under%20Active%20Development-brightgreen" alt="Status">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/GhostPath-Recon%20%7C%20OSINT%20%7C%20Modular-blueviolet?style=for-the-badge&logo=ghost" alt="GhostPath Identity Badge">
</p>

<p align="center">
  <em>A modular, powerful, and fully open-source web reconnaissance toolkit built for <strong>ethical hackers</strong>, <strong>OSINT analysts</strong> and <strong>security researchers</strong>.</em>
</p>

With **GhostPath**, you can **dig through historical URLs**, **hunt down forgotten directories** and **enumerate subdomains from public certificate logs**, all from a single, intuitive CLI interface.

---

## 🛠️ Installation

```bash
# Clone GhostPath
git clone https://github.com/atharvbyadav/GhostPath.git
cd GhostPath

# (Optional but recommended) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install -r requirements.txt
```

---

## 🧭 Usage Overview

```bash
python3 ghostpath/main.py --help
```

This will list all available modules.

For help on a specific module:

```bash
python3 ghostpath/main.py <module> --help
```

Where `<module>` can be:

* `timetrail`
* `certtrack`
* `pathprobe`
* *(More coming soon...)*

---

## 📂 Available Modules

---

### 🌐 TimeTrail – Historical URL Discovery

**Dig through web archives and discover past URLs for a target domain.**

**Supported Sources:**

* Wayback Machine
* URLScan.io
* Common Crawl Index

**Usage:**

```bash
python3 ghostpath/main.py timetrail --target <domain> --source <wayback|urlscan|commoncrawl> [options]
```

**Flags:**

| Flag       | Description                                      |
| ---------- | ------------------------------------------------ |
| `--target` | Target domain (e.g., `example.com`)              |
| `--source` | Data source: `wayback`, `urlscan`, `commoncrawl` |
| `--output` | Save results to a file                           |
| `--format` | Output format: `txt`, `json` or `csv`            |
| `--debug`  | Enable verbose debug output                      |

**Example:**

```bash
python3 ghostpath/main.py timetrail --target example.com --source wayback --output urls.txt --debug
```

---

### 🔎 CertTrack – Passive Subdomain Enumeration

**Extract subdomains from public Certificate Transparency logs using crt.sh**

**Usage:**

```bash
python3 ghostpath/main.py certtrack --target <domain> [options]
```

**Flags:**

| Flag       | Description                            |
| ---------- | -------------------------------------- |
| `--target` | Target domain (e.g., `example.com`)    |
| `--output` | Save results to a file                 |
| `--format` | Output format: `txt`, `json` or `csv`  |
| `--debug`  | Enable debug output                    |

**Example:**

```bash
python3 ghostpath/main.py certtrack --target example.com --format json --debug
```

---

### 🛡️ PathProbe – Active Directory & File Brute-Forcing

**Actively discover hidden directories and files by brute-forcing URL paths.**

**Usage:**

```bash
python3 ghostpath/main.py pathprobe --target <url> --wordlist <file> [options]
```

**Flags:**

| Flag         | Description                                         |
| ------------ | --------------------------------------------------- |
| `--target`   | Full base URL (e.g., `https://example.com`)         |
| `--wordlist` | Path to a wordlist file (one path per line)         |
| `--status`   | HTTP status codes to match (default: `200 301 302`) |
| `--threads`  | Number of concurrent threads (default: 10)          |
| `--output`   | Save results to a file                              |
| `--format`   | Output format: `txt`, `json` or `csv`               |
| `--debug`    | Enable verbose output                               |

**Example:**

```bash
python3 ghostpath/main.py pathprobe --target https://example.com --wordlist wordlists/common.txt --status 200 403 --threads 20 --debug
```

---

### 🛠️ Upcoming Module: DomainScope (Coming Soon 🚧)

**Stay tuned for:**

* WHOIS Lookups
* Geolocation Data
* Reverse DNS
* ASN Details
* DNS Record Enumeration

*DomainScope will focus on passive metadata footprinting from public internet sources.*

---

## 📤 Output Formats

| Format  | Description                                |
| ------- | ------------------------------------------ |
| `.txt`  | Simple, newline-separated                  |
| `.json` | Structured JSON array                      |
| `.csv`  | Easy-to-import CSV format for spreadsheets |

**Example:**

```bash
--output results.json --format json
```

---

## 🐞 Debug Mode – See GhostPath Think in Real-Time

GhostPath includes a powerful `--debug` flag for **any module**, giving you:

✅ Full API endpoints and request parameters
✅ HTTP status codes and responses
✅ Retry attempt details
✅ Internal decision logs

**Example:**

```bash
python3 ghostpath/main.py timetrail --target example.com --source urlscan --debug
```

You’ll get live console feedback like:

```
[DEBUG] Fetching historical URLs for domain: example.com
[DEBUG] URLScan API URL: https://urlscan.io/api/v1/search/?q=domain:example.com
[DEBUG] HTTP 200 Response from URLScan
```

---

## 🔁 Robust Error Handling & Retry Logic

GhostPath handles flaky networks like a champ.

| Module    | Built-in Retry?              |
| --------- | ---------------------------- |
| TimeTrail | ✅ Yes (for all data sources) |
| CertTrack | ✅ Yes (crt.sh API retries)   |
| PathProbe | ✅ Yes (per-target retries)   |

✅ Automatic backoff
✅ Debug logging of failures
✅ Graceful exit after retry exhaustion

---

## 🏗️ Project Structure

```
GhostPath/
├── ghostpath/
│   ├── main.py
│   ├── modules/
│   │   ├── passive/
│   │   │   ├── timetrail.py
│   │   │   └── certtrack.py
│   │   ├── active/
│   │   │   └── pathprobe.py
│   │   └── shared/
│   │       ├── logger.py
│   │       └── output.py
├── requirements.txt
└── README.md
```

---

## 🛣️ Roadmap

✅ Output filtering (keyword, extension based)
✅ API key-based OSINT plugins
✅ Batch multi-target scanning
✅ Exportable JSON schemas for automation
✅ Proxy support

*Want to contribute? Pull requests are welcome!*

---

## ⚖️ Legal & Ethical Disclaimer

GhostPath is a **research-focused and educational web reconnaissance tool**, developed for **security professionals**, **ethical hackers** and **OSINT researchers**.

By using GhostPath, you agree that:

* ✅ You have **explicit and legal authorization** to scan the target systems or domains.
* ✅ You will **never use GhostPath for unauthorized, malicious or illegal activities**.
* ✅ You take **full responsibility** for your actions and their consequences.

> **Reminder:**
> **Unauthorized scanning is illegal and unethical.
> Stay professional. Stay responsible. Stay ethical.**

---

## 👨‍💻 Author

Built with ❤️ and Python by **Atharv Yadav**

🔗 [GitHub – atharvbyadav](https://github.com/atharvbyadav)

---

## 📜 License

GhostPath is distributed under the **BSD 3-Clause License**.

You are free to **use**, **modify** and **redistribute**, provided you comply with the license terms and retain attribution.

For full details, check the [`LICENSE`](./LICENSE) file.

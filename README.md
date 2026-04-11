<h2 align="center">
  <img src="https://raw.githubusercontent.com/atharvbyadav/GhostPath/gh-pages/GhostPath-New.jpeg" alt="GhostPath Logo" width="700"/>
</h2>

<H3>
<p align="center">
  <i><b>GhostPath</b> — A Modern Interactive Reconnaissance Toolkit for Hackers & Security Researchers 🕵️‍♂️</i>
</p>
</H3>

<p align="center">
  <img src="https://img.shields.io/badge/license-BSD%203--Clause-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/type-Passive%20%2F%20Active%20Recon-yellow" alt="Recon Type">
  <img src="https://img.shields.io/badge/modules-TimeTrail%20|%20CertTrack%20|%20PathProbe%20|%20DomainScope-orange" alt="Modules">
  <img src="https://img.shields.io/badge/focus-OSINT%20Recon-red" alt="Focus">
  <img src="https://img.shields.io/badge/debug-Verbose%20Logs%20Available-lightgrey" alt="Debug">
  <img src="https://img.shields.io/badge/platform-Linux%20|%20WSL%20|%20MacOS-lightgreen" alt="Platform">
  <img src="https://img.shields.io/badge/status-Under%20Active%20Development-brightgreen" alt="Status">
</p>

---

## 🧠 What is GhostPath?

**GhostPath** is a professional-grade CLI reconnaissance toolkit designed for cybersecurity researchers, penetration testers and bug bounty hunters. It provides a modular, extensible and interactive shell to run recon operations in an intuitive and streamlined way.

💡 Powered by Python and focused on speed, clarity and results.

---

<p align="center"><i>🕷️ GhostPath — Stealthy. Modular. Effective.</i></p>

---

## ✨ Features

- 🖥️ Textual-powered TUI dashboard with live logs, stats and result tables
- 🔗 Passive, active, intelligence and discovery recon modules
- 🧩 Modular plugin architecture with automatic module loading
- 📁 Output saving in JSON, CSV, HTML and raw session snapshots
- 🚀 Async path probing, JS fetching and directory brute forcing
- 🧾 Certificate transparency & subdomain discovery
- 🌐 Wayback, URLScan and CommonCrawl support
- 🧠 New ParamMiner, JSIntel, DirBrute, TechDetect and subdomain permutation modules
- 💾 Session persistence and export workflows
- 🔧 `pip` - installable for users
- 🔧 `pipx`-installable for global CLI use
- ✅ `--help`, `--version`, module CLI compatibility and structured exports

---

## 🚀 Installation (Recommended: pipx)

Use **pipx** for a clean, isolated global installation:

```bash
# Install pipx (if not already)
sudo apt install pipx
pipx ensurepath
source ~/.bashrc  # or ~/.zshrc

# Install GhostPath
pipx install GhostPath
````

### ✅ Run from anywhere:

```bash
GhostPath
```

Use **pip** for easy and quick installation:

```bash
# install GhostPath
pip install GhostPath
```

If your OS does not support direct pip installation, use a virtual environment for installation

```bash
python3 -m venv venv
source venv/bin/activate
```
> Note that if you use a virtual environment you can only use the tool inside that environment. For global use try **pipx**.

---

<img src="https://raw.githubusercontent.com/atharvbyadav/GhostPath/gh-pages/GhostPath-TerminalLogo.png" alt="GhostPath Terminal Banner" width="100%"/>

---

## 🐍 Running without pipx (Direct Script Mode)

If you prefer not to use pipx or pip, you can run GhostPath directly using Python:

### 1. Clone the repository

```bash
git clone https://github.com/atharvbyadav/GhostPath.git
cd GhostPath
```

### 2. (Optional) Create a virtual environment

> Highly recommended to isolate dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the GhostPath dashboard

```bash
python3 main_cli.py
```

This launches the GhostPath v3.0 TUI dashboard by default.

---

## 💻 TUI Usage

Run:

```bash
ghostpath
```

Keyboard shortcuts:

- `TAB` switch panels
- `ENTER` run selected module
- `S` save current session
- `E` export the latest results
- `R` rerun the selected module
- `Q` quit
- `/` focus the target/search input

The TUI includes:

- module sidebar
- live result table
- log stream with levels
- status and summary stats panels

---

## 💻 CLI Usage Overview

Existing command-style usage remains supported:

```bash
ghostpath timetrail example.com
ghostpath domainscope example.com
ghostpath pathprobe https://example.com --threads 50
ghostpath certtrack example.com --output certs.json --format json
```

---

## 🧩 Modules

### 🕰️ `timetrail`

Fetch historical URLs from:

* Common Crawl *(default)*
* Wayback Machine
* URLScan.io

```bash
timetrail --target example.com
timetrail --target example.com --source wayback --output urls.json --format json
```

---

### 🌐 `domainscope`

Find subdomains and related DNS data.

```bash
domainscope --target example.com
domainscope --target example.com --output domains.txt
```

---

### 📜 `certtrack`

Gather subdomains from SSL/TLS certificate transparency logs.

```bash
certtrack --target example.com
certtrack --target example.com --output certs.csv --format csv
```

---

### 🔓 `pathprobe`

Actively probe common paths/endpoints on a web app using HTTP requests.

```bash
pathprobe --target https://example.com
pathprobe --target https://example.com --wordlist lists/path-wordlist.txt --output result.json --format json
```

> If no wordlist is passed, it will fallback to:
> `GhostPath/lists/path-wordlist.txt`

---

### 🧪 `paramminer`

Extract parameters from wayback URLs, JavaScript files and HTML forms:

```bash
ghostpath paramminer example.com
```

---

### 🧠 `jsintel`

Extract endpoints, tokens, secrets and internal domains from JavaScript:

```bash
ghostpath jsintel https://example.com
```

---

### 📂 `dirbrute`

Asynchronously brute force common directories:

```bash
ghostpath dirbrute https://example.com
```

---

### 🧬 `sub_permuter`

Generate likely subdomain permutations:

```bash
ghostpath sub_permuter example.com
```

---

### 🧱 `techdetect`

Detect common server, framework, CMS and CDN indicators:

```bash
ghostpath techdetect https://example.com
```

---

## 🧪 Output Formats

All modules support output saving in:

* ✅ `.json`
* ✅ `.csv`
* ✅ `.html`
* ✅ raw session snapshots

Just pass:

```bash
--output filename --format json|csv|html|txt
```

Export an existing session or JSON payload:

```bash
ghostpath export outputs/raw/session_example.com_latest.json --format html
```

---

## 💾 Sessions

Save and load the latest session for a target:

```bash
ghostpath session save example.com
ghostpath session load example.com
```

---

## 📦 Version & Self-Update

### Check current version:

```bash
ghostpath> version
```

---

### Reinstall / Update (via pipx):

```bash
pipx reinstall GhostPath
```

---

## 📜 License

```text
BSD 3-Clause License

Copyright (c) 2025, Atharv Yadav
All rights reserved.
```

> 📄 See the [LICENSE](LICENSE) file for full license terms.

---

## 🤝 Contributing

We welcome your pull requests, feature ideas and improvements to make **GhostPath** even better! Here's how to contribute:

1. **Fork** the repository
2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/yourusername/GhostPath.git
   cd GhostPath
   ```
3. **Create a new branch** for your changes:

   ```bash
   git checkout -b feature/your-feature
   ```
4. Make your changes and **commit**:

   ```bash
   git commit -m "Add: your feature/fix summary"
   git push origin feature/your-feature
   ```
5. Open a **Pull Request** on GitHub 📬

> Please follow best practices and write clear commit messages 🙌

---

## 👨‍💻 Author

```bash
┌─[ Coded with ☕ + ⚡ by Atharv Yadav ]
│
├─🛠️  Creator of GhostPath
├─🌐  https://github.com/atharvbyadav
└─📧  uuwr5t1s [at] duck [dot] com
      { _Looks suspicious? Good. It’s mine. The ducks work for me. 🦆💻_ }
```

> *"I don’t just scan — I haunt networks."* 👻

<p>
  🔗 <a href="https://github.com/atharvbyadav" target="_blank">GitHub: @atharvbyadav</a> <br>
  ✉️ <a href="mailto:uuwr5t1s@duck.com">Email Me</a>
</p>

---

<h2 align="center">
  <img src="https://github.com/atharvbyadav/GhostPath/blob/gh-pages/GhostPath-New.png" alt="GhostPath Logo" width="700"/>
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

## ✨ Features

- 🔍 Interactive hacker-style CLI shell
- 🔗 Passive and active recon modules
- 🧩 Modular architecture with shared utilities
- 📁 Output saving in TXT, JSON, CSV
- 🚀 Multithreaded path probing with live feedback
- 🧾 Certificate transparency & subdomain discovery
- 🌐 Wayback, URLScan and CommonCrawl support
- 🧠 Built-in wordlist fallback & auto-detection
- 🔧 `pipx`-installable for global CLI use
- ✅ `--help`, `--version` and `update` command support

---

## 🚀 Installation (Recommended: pipx)

Use **pipx** for a clean, isolated global installation:

```bash
# Install pipx (if not already)
sudo apt install pipx
pipx ensurepath
source ~/.bashrc  # or ~/.zshrc

# Clone and install GhostPath
git clone https://github.com/atharvbyadav/GhostPath.git
cd GhostPath
pipx install .
````

### ✅ Run from anywhere:

```bash
GhostPath
```

---

<img src="https://github.com/atharvbyadav/GhostPath/blob/gh-pages/GhostPath-TerminalLogo.png" alt="GhostPath Terminal Banner" width="100%"/>

---

## 🐍 Running without pipx (Direct Script Mode)

If you prefer not to use pipx, you can run GhostPath directly using Python:

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

### 4. Run the GhostPath CLI shell

```bash
python3 main_cli.py
```

---

## 💻 Usage Overview

Once inside the shell:

```bash
ghostpath> help
```

You’ll see:

```
🧩 Available GhostPath Commands:
  timetrail      → Fetch historical URLs from archives (Wayback, URLScan, Common Crawl)
  domainscope    → Discover subdomains & DNS profiling
  pathprobe      → Actively probe directories and endpoints
  certtrack      → Get subdomains from public SSL/TLS certs
  version        → Show current installed version
  clear          → Clear the screen
  help           → Show this help menu
  exit           → Exit GhostPath CLI
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

## 🧪 Output Formats

All modules support output saving in:

* ✅ `.txt`
* ✅ `.json`
* ✅ `.csv`

Just pass:

```bash
--output filename --format txt|json|csv
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

<p align="center"><i>🕷️ GhostPath — Stealthy. Modular. Effective.</i></p>

---
# 🕵️‍♂️ GhostPath — Trace the Web's Forgotten Trails

GhostPath is your **silent recon companion** — a **powerful, passive reconnaissance toolkit** that unearths forgotten traces of a target domain without making a sound.

Designed for **ethical hackers, bug bounty hunters, and red teams**, GhostPath reveals historical URLs, forgotten subdomains, and digital footprints using only **open-source intelligence (OSINT)** techniques — **no API keys required, no noise generated**.

Lightweight, fast, and modular, GhostPath helps you map your target’s web shadow — all with just a single command.

---

### 🧩 Capabilities at a Glance

<p align="center">
  <a href="#">
    <img alt="Passive Recon" src="https://img.shields.io/badge/Passive_Recon-✔️-brightgreen?style=for-the-badge" />
  </a>
  <a href="#">
    <img alt="Subdomain Enumeration" src="https://img.shields.io/badge/Subdomain_Enumeration-✔️-blue?style=for-the-badge" />
  </a>
  <a href="#">
    <img alt="Historical URL Discovery" src="https://img.shields.io/badge/Historical_URL_Discovery-✔️-orange?style=for-the-badge" />
  </a>
  <a href="#">
    <img alt="No API Keys Required" src="https://img.shields.io/badge/No_API_Keys_Required-✔️-lightgrey?style=for-the-badge" />
  </a>
  <a href="https://www.python.org/downloads/">
    <img alt="Python 3.7+" src="https://img.shields.io/badge/Python-3.7+-blue.svg?style=for-the-badge&logo=python" />
  </a>
  <a href="#">
    <img alt="Supported OS" src="https://img.shields.io/badge/OS-Linux%20|%20macOS%20|%20Windows-lightgrey.svg?style=for-the-badge" />
  </a>
  <a href="https://opensource.org/licenses/BSD-3-Clause">
    <img alt="License" src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=for-the-badge" />
  </a>
</p>

---

## 🚀 Features

- 🔍 **Passive Reconnaissance:** Gather intelligence without direct interaction with the target.
- 🌐 **Subdomain Enumeration:** Discover subdomains via multiple sources and APIs.
- 📜 **Historical URL Discovery:** Fetch archived URLs from Wayback Machine and others.
- 🔑 **No API Keys Required:** Ready-to-use without any setup hassle.
- 🧹 **Deduplication:** Removes duplicate URLs and subdomains for clean output.
- 📦 **Modular Architecture:** Easily extendable with fetchers and utilities.
- 🐍 **Python 3.7+ Compatible:** Works on all major OS (Linux, macOS, Windows).
- 🛠️ **CLI Tool:** Simple command-line interface for quick scans.

---
> “Reconnaissance is the foundation of a secure attack and an effective defense.”
> — *Atharv Yadav*
---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/atharvbyadav/GhostPath.git
cd GhostPath

# (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

---

## ⚙️ Usage

```bash
python main.py --domain example.com
```

Replace `example.com` with your target domain.

### Options

* `--domain` : Specify the target domain for reconnaissance.
* `--output` : (Optional) Specify a file to save the results.
* `--verbose`: Enable detailed output.

*For full options, run:*

```bash
python main.py --help
```

---

## 📂 Project Structure

```
GhostPath/
├── fetchers/          # Modules to fetch data from different passive sources
│   ├── subdomains.py  # Subdomain enumeration logic
│   └── wayback.py     # Historical URL discovery from Wayback Machine
├── utils/             # Utility modules for deduplication, parsing, etc.
│   └── dedup.py       # Deduplication functions
├── main.py            # Main CLI entry point
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests for bugs, improvements, or new fetchers.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **BSD 3-Clause License** — see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

Have ideas, suggestions, or just want to connect?

- **👨‍💻 Author**: **Atharv Yadav**
- **📧 Email**: [uuwr5t1s@duck.com](mailto:uuwr5t1s@duck.com)  
  _Looks suspicious? Good. It’s mine. The ducks work for me. 🦆💻_
- **🌐 Website**: [atharvbyadav.github.io](https://atharvbyadav.github.io)
- **🐙 GitHub**: [@atharvbyadav](https://github.com/atharvbyadav)
- **🧠 Connect**: [LinkedIn](https://www.linkedin.com/in/atharvbyadav/) · [X](https://x.com/AtharvYadavB)

> *Collaboration is the backbone of innovation. Reach out — let’s build better tools together.*

---




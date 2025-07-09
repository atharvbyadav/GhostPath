#!/usr/bin/env python3

import readline
import shlex
import os
import sys
from ghostpath.version import __version__
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

COMMANDS = ["timetrail", "domainscope", "pathprobe", "certtrack", "clear", "help", "exit", "output", "target", "wordlist", "threads", "format", "debug"]

readline.parse_and_bind("tab: complete")
readline.set_completer(
    lambda text, state: [cmd for cmd in COMMANDS if cmd.startswith(text)][state]
    if state < len([cmd for cmd in COMMANDS if cmd.startswith(text)]) else None
)

def show_banner():
    banner = r"""
   ▒█████   ██░ ██  ▒█████   ██████ ▄▄▄█████▓     ▒███████▒ ▄▄▄      ████████  ██░ ██ 
  ▒██▒      ██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒    ▒ ██▒ ██░▒████▄   ▒██ ██ ▒▒ ▓██░ ██▒    
  ▒██░████▒▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░    ░ ██████ ▒██  ▀█▄  ░▓ ██ ▒░ ▒██▀▀██░
  ▒██ ▒▓██░░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░     ▒ ██▒   ░░██▄▄▄▄██  ▒ ██ ░░▒░▓█ ░██ 
  ░ ████▓▒░░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░     ▒ ██   ▒▒ ▓█   ▓██▒▒░ ██ ▒ ▒▒░▓█▒░██▓
  ░ ▒░▒░▒░  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░         ▒▓▒ ▒ ░ ▒▒   ▓▒█░▒░▒▓▒ ▒ ░ ▒ ░░▒░▒
    ░ ▒ ▒░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░        ░ ░▒  ░ ░  ▒   ▒▒ ░░ ░▒▒ ░ ░ ▒ ░▒░ ░ 
  ░ ░ ░ ▒   ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░          ░  ░  ░    ░   ▒   ░  ░▒ ░   ░  ░░ ░  
      ░ ░   ░  ░  ░    ░ ░        ░                       ░        ░  ░    ░ ░   ░  ░  ░
"""
    print(banner)

def show_help():
    print("""
🧩 Available GhostPath Commands:
  timetrail      → Fetch historical URLs from archives (Wayback, URLScan, Common Crawl)
  domainscope    → Discover subdomains & DNS profiling
  pathprobe      → Actively probe directories and endpoints
  certtrack      → Get subdomains from public SSL/TLS certs
  version        → Show current installed version
  clear          → Clear the screen
  help           → Show this help menu
  exit           → Exit GhostPath CLI
""")

def run_command(command, args):
    try:
        if command == "timetrail":
            from ghostpath.modules.passive import timetrail
            parser = timetrail.arg_parser()
            if "--help" in args or "-h" in args:
                parser.print_help() 
                return
            parsed_args = parser.parse_args(args)
            timetrail.run(parsed_args)

        elif command == "domainscope":
            from ghostpath.modules.active import domainscope
            parser = domainscope.arg_parser()
            if "--help" in args or "-h" in args:
                parser.print_help()
                return
            parsed_args = parser.parse_args(args)
            domainscope.run(parsed_args)

        elif command == "pathprobe":
            from ghostpath.modules.active import pathprobe
            parser = pathprobe.arg_parser()
            if "--help" in args or "-h" in args:
                parser.print_help()
                return
            parsed_args = parser.parse_args(args)
            pathprobe.run(parsed_args)

        elif command == "certtrack":
            from ghostpath.modules.passive import certtrack
            parser = certtrack.arg_parser()
            if "--help" in args or "-h" in args:
                parser.print_help()
                return
            parsed_args = parser.parse_args(args)
            certtrack.run(parsed_args)

    except SystemExit as e:
        if e.code != 0: 
            print("[!] Invalid arguments. Type 'help' for usage.")
    except Exception as e:
        print(f"[!] Error: {e}")


def main():
    show_banner()
    print(f"👻 GhostPath Interactive Recon Shell | Developed by @atharvbyadav | Version {__version__} \nType 'help' for options\n")

    while True:
        try:
            user_input = input("ghostpath> ").strip()
            if not user_input:
                continue
            if user_input in ["--version", "-v", "version"]:
                print(f"GhostPath version {__version__}")
                continue

            if user_input == "update":
                print("[*] Updating GhostPath using pipx...")
                os.system("pipx reinstall GhostPath")
                continue

            args = shlex.split(user_input)
            command = args[0]
            cmd_args = args[1:]

            if command == "exit":
                print("[*] Exiting GhostPath.")
                break
            elif command == "clear":
                os.system("cls" if os.name == "nt" else "clear")
            elif command == "help":
                show_help()
            elif command in COMMANDS:
                run_command(command, cmd_args)
            else:
                print(f"[!] Unknown command: '{command}'. Type 'help'.")

        except KeyboardInterrupt:
            print("\n[!] Use 'exit' to leave the shell.")
        except Exception as e:
            print(f"[!] Unexpected error: {e}")

if __name__ == "__main__":
    main()

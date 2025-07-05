import argparse
import sys

from modules.passive import timetrail, certtrack
from modules.active import pathprobe, domainscope

def main():
    parser = argparse.ArgumentParser(
        prog="ghostpath",
        description="GhostPath - OSINT & Active Recon Toolkit (2025 Edition)"
    )

    subparsers = parser.add_subparsers(
        dest="module",
        title="Modules",
        description="Choose a module to run",
        help="Use 'ghostpath <module> --help' for module-specific options."
    )

    # ----- Passive Modules -----
    # TimeTrail Module (Historical URLs)
    timetrail_parser = subparsers.add_parser(
        "timetrail",
        help="Historical URL Discovery (Passive)"
    )
    timetrail.add_arguments(timetrail_parser)

    # CertTrack Module (Subdomains from cert transparency)
    certtrack_parser = subparsers.add_parser(
        "certtrack",
        help="Subdomain Discovery from Certificate Transparency Logs (Passive)"
    )
    certtrack.add_arguments(certtrack_parser)

    # ----- Active Modules -----
    # PathProbe Module (Active endpoint probing)
    pathprobe_parser = subparsers.add_parser(
        "pathprobe",
        help="Hidden Path Discovery (Active)"
    )
    pathprobe.add_arguments(pathprobe_parser)

    # DomainScope Module (Subdomain brute force)
    domainscope_parser = subparsers.add_parser(
        "domainscope",
        help="Subdomain Wordlist Discovery (Active)"
    )
    domainscope.add_arguments(domainscope_parser)

    # Parse arguments
    args = parser.parse_args()

    # No module selected
    if args.module is None:
        parser.print_help()
        sys.exit(1)

    # Module Dispatcher
    if args.module == "timetrail":
        timetrail.run(args)
    elif args.module == "certtrack":
        certtrack.run(args)
    elif args.module == "pathprobe":
        pathprobe.run(args)
    elif args.module == "domainscope":
        domainscope.run(args)
    else:
        print(f"Unknown module: {args.module}")
        sys.exit(1)

if __name__ == "__main__":
    main()

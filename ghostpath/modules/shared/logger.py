import sys

debug_enabled = False

def enable_debug():
    global debug_enabled
    debug_enabled = True

def debug(message):
    if debug_enabled:
        print(f"[DEBUG] {message}", file=sys.stderr)

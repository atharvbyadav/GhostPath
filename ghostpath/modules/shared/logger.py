DEBUG_ENABLED = False

def enable_debug():
    global DEBUG_ENABLED
    DEBUG_ENABLED = True

def debug(message):
    if DEBUG_ENABLED:
        print(f"[DEBUG] {message}")

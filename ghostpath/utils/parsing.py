"""Parsing helpers."""

from __future__ import annotations

import re
from urllib.parse import urlparse


PARAMETER_REGEX = re.compile(r"[?&]([A-Za-z0-9_\-]+)=")
ENDPOINT_REGEX = re.compile(r"""(?:"|')((?:/[A-Za-z0-9._\-/]+|https?://[^"' ]+))(?:"|')""")
SECRET_REGEX = re.compile(
    r"""(?ix)
    (?:
      api[_-]?key|
      secret|
      token|
      access[_-]?key|
      auth[_-]?token
    )
    \s*[:=]\s*
    (?:"|')([A-Za-z0-9_\-]{8,})(?:"|')
    """
)


def extract_domain(value: str) -> str:
    parsed = urlparse(value if "://" in value else f"https://{value}")
    return parsed.netloc or parsed.path


def ensure_url(value: str) -> str:
    return value if "://" in value else f"https://{value}"

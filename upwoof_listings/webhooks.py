"""Verifying the signatures on UpWoof's outbound webhook deliveries.

Each delivery is signed with the subscription's secret, `Base64(HMAC-SHA256(secret, message))`:

* `X-Upwoof-Signature` signs the raw request body alone. It proves who sent the delivery, not when.
* `X-Upwoof-Timestamp` is the send time in Unix seconds, and `X-Upwoof-Timestamped-Signature` signs
  `"<timestamp>.<body>"`. Prefer `verify_timestamped_signature`, which also rejects a delivery whose
  timestamp is outside the tolerance window, so a captured request can't be replayed later.

Always pass the raw body exactly as received, before any JSON parsing.
"""
import base64
import hashlib
import hmac
import time
from typing import Optional, Union

SIGNATURE_HEADER = 'X-Upwoof-Signature'
TIMESTAMP_HEADER = 'X-Upwoof-Timestamp'
TIMESTAMPED_SIGNATURE_HEADER = 'X-Upwoof-Timestamped-Signature'
DELIVERY_ID_HEADER = 'X-Upwoof-Webhook-Id'
DEFAULT_TOLERANCE_SECONDS = 300

Bytesish = Union[str, bytes]


def _to_bytes(value: Bytesish) -> bytes:
    return value if isinstance(value, bytes) else str(value).encode('utf-8')


def compute_signature(message: Bytesish, secret: Bytesish) -> str:
    digest = hmac.new(_to_bytes(secret), _to_bytes(message), hashlib.sha256).digest()
    return base64.b64encode(digest).decode('ascii')


def verify_signature(payload: Bytesish, signature: Optional[str], secret: Bytesish) -> bool:
    """True when `signature` (the X-Upwoof-Signature header) matches the raw `payload`."""
    if not signature or not secret:
        return False
    return hmac.compare_digest(compute_signature(payload, secret), signature)


def verify_timestamped_signature(payload: Bytesish, timestamp: Optional[Union[str, int]],  # pylint: disable=too-many-arguments
                                 signature: Optional[str], secret: Bytesish, *,
                                 tolerance: int = DEFAULT_TOLERANCE_SECONDS,
                                 now: Optional[float] = None) -> bool:
    """True when `signature` (X-Upwoof-Timestamped-Signature) matches `"<timestamp>.<payload>"` and
    `timestamp` (X-Upwoof-Timestamp) is within `tolerance` seconds of `now` (default: the current time),
    either side. A missing, malformed, stale or future timestamp is rejected."""
    if not signature or not secret or timestamp is None:
        return False
    raw_timestamp = str(timestamp).strip()
    try:
        sent_at = int(raw_timestamp)
    except ValueError:
        return False
    current = time.time() if now is None else now
    if abs(int(current) - sent_at) > tolerance:
        return False
    message = _to_bytes(raw_timestamp) + b'.' + _to_bytes(payload)
    return hmac.compare_digest(compute_signature(message, secret), signature)

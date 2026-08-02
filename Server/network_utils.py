"""
network_utils.py
Simple helpers for sending / receiving JSON over TCP.
"""

import json
from config import BUFFER_SIZE


def send_json(sock, data: dict):
    """Send a Python dict as JSON."""
    msg = json.dumps(data).encode("utf-8")
    sock.sendall(msg)


def recv_json(sock):
    """Receive JSON and return a Python dict. Returns None on empty/closed."""
    data = sock.recv(BUFFER_SIZE)
    if not data:
        return None
    try:
        return json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        return {"status": "error", "msg": "bad json"}

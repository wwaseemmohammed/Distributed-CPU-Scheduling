"""
server.py
Main server entry point.
Each new connection runs in its own thread.
When the client disconnects, that thread ends.
"""

import socket
import threading

from config import HOST, PORT, MAX_CLIENTS
from client_handler import handle_client
import client_handler as ch

# load scheduler if available
try:
    from scheduler import Scheduler
    ch.Scheduler = Scheduler
except ImportError:
    ch.Scheduler = None


def start_server():
    print("=" * 50)
    print("  Distributed CPU Scheduling Server")
    print("=" * 50)
    print(f"Listening on {HOST}:{PORT}")
    print("Each connection -> one thread")
    print("Disconnect -> thread ends")
    if ch.Scheduler is None:
        print("WARNING: scheduler.py not found")
    print("=" * 50)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(MAX_CLIENTS)
    print("[SERVER] Waiting for connection...\n")

    try:
        while True:
            conn, addr = srv.accept()
            # one thread per connection
            t = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            )
            t.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Stopped.")
    finally:
        srv.close()


if __name__ == "__main__":
    start_server()

"""
client_handler.py
One connection = one thread.

- While the connection stays open: all sent processes
  are stored in the same list on this thread.
- When the client disconnects: this thread ends.
"""

from process import Process
from network_utils import send_json, recv_json

# set by server.py if scheduler exists
Scheduler = None


def handle_client(conn, addr):
    cid = f"{addr[0]}:{addr[1]}"
    print(f"[SERVER] Connected: {cid} (new thread)")

    # processes for THIS connection only (same thread)
    my_processes = []
    my_results = {}
    my_results_ready = False

    try:
        while True:
            msg = recv_json(conn)
            if msg is None:
                # connection closed -> leave loop -> thread ends
                break

            action = msg.get("action")

            # send processes (can be called many times on same connection)
            if action == "send_processes":
                plist = msg.get("processes", [])
                newp = [Process.from_dict(p) for p in plist]
                my_processes.extend(newp)

                print(f"[SERVER] {cid} sent {len(newp)} processes "
                      f"(total on this connection: {len(my_processes)})")
                for p in newp:
                    print(f"         {p}")

                send_json(conn, {
                    "status": "ok",
                    "msg": f"received {len(newp)} processes",
                    "queue_size": len(my_processes)
                })

            elif action == "run_scheduling":
                if not my_processes:
                    send_json(conn, {
                        "status": "error",
                        "msg": "no processes. send some first."
                    })
                    continue

                if Scheduler is None:
                    send_json(conn, {
                        "status": "error",
                        "msg": "scheduler.py not found"
                    })
                    continue

                print(f"\n[SERVER] Running Scheduler for {cid} "
                      f"({len(my_processes)} processes) ...")

                scheduler = Scheduler()
                results = scheduler.run_all(list(my_processes))
                my_results = results
                my_results_ready = True

                for name, res in results.items():
                    avg = res.get("avg_waiting_time", "?")
                    print(f"  {name:25} Avg WT = {avg}")
                print()

                send_json(conn, {
                    "status": "ok",
                    "results": results
                })

            elif action == "get_results":
                if my_results_ready:
                    send_json(conn, {
                        "status": "ok",
                        "results": my_results
                    })
                else:
                    send_json(conn, {
                        "status": "error",
                        "msg": "no results yet"
                    })

            elif action == "clear_queue":
                my_processes.clear()
                my_results = {}
                my_results_ready = False
                print(f"[SERVER] {cid} cleared queue")
                send_json(conn, {
                    "status": "ok",
                    "msg": "queue cleared"
                })

            elif action == "status":
                send_json(conn, {
                    "status": "ok",
                    "queue_size": len(my_processes),
                    "results_ready": my_results_ready,
                    "scheduler_available": Scheduler is not None
                })

            else:
                send_json(conn, {
                    "status": "error",
                    "msg": "unknown action"
                })

    except (ConnectionResetError, BrokenPipeError, OSError) as e:
        print(f"[SERVER] Connection lost with {cid}: {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass
        # thread ends here
        print(f"[SERVER] Thread ended for {cid}")

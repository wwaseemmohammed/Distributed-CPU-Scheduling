"""
client.py
Simple TCP Client. Console menu only.
Each Client sees only its own results.
"""

import socket
import json
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Server"))
from config import CLIENT_HOST, PORT, BUFFER_SIZE


def generate_processes(client_id, num=5):
    processes = []
    for i in range(num):
        p = {
            "pid": random.randint(100, 999),
            "arrival_time": random.randint(0, 10),
            "burst_time": random.randint(1, 10),
            "priority": random.randint(1, 5),
            "client_id": client_id
        }
        processes.append(p)
    return processes


def send_message(sock, msg):
    data = json.dumps(msg).encode("utf-8")
    sock.sendall(data)
    reply = sock.recv(BUFFER_SIZE)
    return json.loads(reply.decode("utf-8"))


def print_gantt(algo_name, gantt):
    """Print Gantt in a different visual style from typical | P1 | P2 | format."""
    if not gantt:
        return

    print(f"\n  >> Timeline  [{algo_name}]")
    print("  " + "-" * 52)

    # row 1: process blocks as solid bars with pid inside
    line = "  "
    for seg in gantt:
        length = max(1, seg["end"] - seg["start"])
        # width proportional but capped for console
        width = min(max(length * 2, 4), 14)
        label = f"P{seg['pid']}"
        # center label in the bar
        pad = width - len(label)
        left = pad // 2
        right = pad - left
        block = "[" + ("=" * left) + label + ("=" * right) + "]"
        line += block
    print(line)

    # row 2: time markers under each segment start
    time_line = "  "
    for seg in gantt:
        length = max(1, seg["end"] - seg["start"])
        width = min(max(length * 2, 4), 14) + 2  # +2 for brackets
        marker = str(seg["start"])
        time_line += marker + " " * (width - len(marker))
    # final end time
    if gantt:
        time_line += str(gantt[-1]["end"])
    print(time_line)
    print("  " + "-" * 52)


def print_results(results):
    print("\n")
    print("*" * 58)
    print("          SCHEDULING RESULTS (this client only)")
    print("*" * 58)

    summary_rows = []

    for algo, data in results.items():
        print(f"\n{'~' * 58}")
        print(f"  Algorithm :: {algo}")
        print(f"{'~' * 58}")

        details = data.get("details", [])
        if details:
            print(f"  {'PID':>6}  {'Wait':>6}  {'TAT':>6}  {'Finish':>7}")
            print(f"  {'------':>6}  {'------':>6}  {'------':>6}  {'-------':>7}")
            for d in details:
                print(f"  {d.get('pid'):>6}  {d.get('waiting_time'):>6}  "
                      f"{d.get('turnaround_time'):>6}  {d.get('completion_time'):>7}")

        avg_wt = data.get("avg_waiting_time", 0)
        avg_tat = data.get("avg_turnaround_time", 0)
        print(f"\n  >> Avg Waiting Time     = {avg_wt}")
        print(f"  >> Avg Turnaround Time  = {avg_tat}")

        summary_rows.append((algo, avg_wt, avg_tat))

        # Gantt chart (different style)
        gantt = data.get("gantt", [])
        print_gantt(algo, gantt)

    # comparison strip at the end
    print(f"\n{'*' * 58}")
    print("  QUICK COMPARE  (Avg Waiting / Avg Turnaround)")
    print(f"{'*' * 58}")
    print(f"  {'Algorithm':<28} {'Wait':>8} {'TAT':>8}")
    print(f"  {'-' * 28} {'-' * 8} {'-' * 8}")
    for name, wt, tat in summary_rows:
        print(f"  {name:<28} {wt:>8} {tat:>8}")
    print(f"{'*' * 58}\n")


def main():
    client_id = f"Client_{random.randint(1, 99)}"
    print("=" * 50)
    print("  CPU Scheduling Client")
    print("=" * 50)
    print(f"Client ID : {client_id}")
    print(f"Connecting to {CLIENT_HOST}:{PORT} ...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((CLIENT_HOST, PORT))
        print("Connected. You will only see YOUR own results.\n")
    except Exception as e:
        print(f"Cannot connect: {e}")
        print("Make sure server is running first.")
        return

    while True:
        print("\n----- Menu -----")
        print("1. Generate & send processes (added to your list)")
        print("2. Run scheduling on YOUR processes only")
        print("3. Get YOUR last results")
        print("4. Clear YOUR process list")
        print("5. Status")
        print("6. Exit (disconnect -> server thread ends)")
        choice = input("Choose (1-6): ").strip()

        if choice == "1":
            n = input("How many processes? (default 5): ").strip()
            n = int(n) if n.isdigit() else 5
            procs = generate_processes(client_id, n)
            print("Generated processes:")
            for p in procs:
                print(f"  {p}")
            resp = send_message(sock, {"action": "send_processes", "processes": procs})
            print("Server reply:", resp.get("msg", resp),
                  "| your queue:", resp.get("your_queue_size"))

        elif choice == "2":
            print("Running algorithms on YOUR processes only...")
            resp = send_message(sock, {"action": "run_scheduling"})
            if resp.get("status") == "ok":
                print_results(resp["results"])
            else:
                print("Error:", resp.get("msg"))

        elif choice == "3":
            resp = send_message(sock, {"action": "get_results"})
            if resp.get("status") == "ok":
                print_results(resp["results"])
            else:
                print("Error:", resp.get("msg"))

        elif choice == "4":
            resp = send_message(sock, {"action": "clear_queue"})
            print("Server reply:", resp.get("msg", resp))

        elif choice == "5":
            resp = send_message(sock, {"action": "status"})
            print("Status:", resp)

        elif choice == "6":
            print("Disconnecting... (server will end your thread)")
            break
        else:
            print("Invalid choice.")

    sock.close()
    print("Bye.")


if __name__ == "__main__":
    main()

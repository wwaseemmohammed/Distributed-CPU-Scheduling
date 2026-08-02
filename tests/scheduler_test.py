import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "Server"))

from process import Process
from scheduler import Scheduler
from scheduler.fcfs import fcfs
from scheduler.sjf import sjf
from scheduler.priority import priority
from scheduler.round_robin import round_robin


def mk(pid, arrival, burst, prio):
    return Process(pid, arrival, burst, prio, "Client_1")


def approx(a, b):
    return abs(a - b) < 0.01


def test_fcfs():
    procs = [mk(1, 0, 24, 1), mk(2, 0, 3, 1), mk(3, 0, 3, 1)]
    r = fcfs(procs)
    assert approx(r.avg_waiting_time(), 17.0), r.avg_waiting_time()


def test_sjf_preemptive():
    procs = [mk(1, 0, 8, 1), mk(2, 1, 4, 1), mk(3, 2, 9, 1), mk(4, 3, 5, 1)]
    r = sjf(procs)
    assert approx(r.avg_waiting_time(), 6.5), r.avg_waiting_time()


def test_priority_nonpreemptive():
    procs = [mk(1, 0, 10, 3), mk(2, 0, 1, 1), mk(3, 0, 2, 4),
             mk(4, 0, 1, 5), mk(5, 0, 5, 2)]
    r = priority(procs)
    assert approx(r.avg_waiting_time(), 8.2), r.avg_waiting_time()


def test_round_robin():
    procs = [mk(1, 0, 5, 2), mk(2, 0, 3, 1), mk(3, 0, 1, 3)]
    r = round_robin(procs, 2)
    assert approx(r.avg_waiting_time(), 4.33), r.avg_waiting_time()


def test_run_all_contract():
    procs = [mk(1, 0, 5, 2), mk(2, 1, 3, 1), mk(3, 2, 8, 3), mk(4, 3, 6, 2)]
    results = Scheduler().run_all(procs)
    assert set(results.keys()) == {
        "FCFS", "SJF (Preemptive)",
        "Priority (Non-Preemptive)", "Round Robin (q=2)"
    }
    json.dumps(results)
    for data in results.values():
        assert "avg_waiting_time" in data
        assert "avg_turnaround_time" in data
        assert "details" in data and "gantt" in data
        for d in data["details"]:
            for k in ("pid", "waiting_time", "turnaround_time", "completion_time"):
                assert k in d
        for seg in data["gantt"]:
            for k in ("start", "end", "pid"):
                assert k in seg


def run():
    tests = [test_fcfs, test_sjf_preemptive, test_priority_nonpreemptive,
             test_round_robin, test_run_all_contract]
    for t in tests:
        t()
        print("PASS  " + t.__name__)
    print(str(len(tests)) + "/" + str(len(tests)) + " tests passed")


if __name__ == "__main__":
    run()

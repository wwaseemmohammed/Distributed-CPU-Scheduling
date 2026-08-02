from .result import Result


def priority(processes):
    result = Result("Priority (Non-Preemptive)")
    procs = sorted(processes, key=lambda p: (p.arrival_time, p.pid))
    n = len(procs)
    done = set()
    completion = {}
    time = 0
    while len(done) < n:
        ready = [p for p in procs
                 if p.arrival_time <= time and p.pid not in done]
        if not ready:
            time = min(p.arrival_time for p in procs if p.pid not in done)
            continue
        cur = min(ready, key=lambda p: (p.priority, p.arrival_time, p.pid))
        start = time
        time += cur.burst_time
        completion[cur.pid] = time
        result.gantt.append({"start": start, "end": time, "pid": cur.pid})
        done.add(cur.pid)
    for p in sorted(procs, key=lambda p: p.pid):
        c = completion[p.pid]
        turnaround = c - p.arrival_time
        waiting = turnaround - p.burst_time
        result.add_detail(p.pid, p.arrival_time, p.burst_time,
                          waiting, turnaround, c)
    return result

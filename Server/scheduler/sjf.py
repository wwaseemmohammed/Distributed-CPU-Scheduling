from .result import Result


def sjf(processes):
    result = Result("SJF (Preemptive)")
    procs = list(processes)
    n = len(procs)
    remaining = {p.pid: p.burst_time for p in procs}
    completion = {}
    done = 0
    time = 0
    while done < n:
        ready = [p for p in procs
                 if p.arrival_time <= time and remaining[p.pid] > 0]
        if not ready:
            time += 1
            continue
        cur = min(ready, key=lambda p: (remaining[p.pid], p.arrival_time, p.pid))
        if (result.gantt and result.gantt[-1]["pid"] == cur.pid
                and result.gantt[-1]["end"] == time):
            result.gantt[-1]["end"] = time + 1
        else:
            result.gantt.append({"start": time, "end": time + 1, "pid": cur.pid})
        remaining[cur.pid] -= 1
        time += 1
        if remaining[cur.pid] == 0:
            completion[cur.pid] = time
            done += 1
    for p in sorted(procs, key=lambda p: p.pid):
        c = completion[p.pid]
        turnaround = c - p.arrival_time
        waiting = turnaround - p.burst_time
        result.add_detail(p.pid, p.arrival_time, p.burst_time,
                          waiting, turnaround, c)
    return result

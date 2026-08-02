from .result import Result


def round_robin(processes, quantum=2):
    result = Result("Round Robin (q=2)")
    procs = sorted(processes, key=lambda p: (p.arrival_time, p.pid))
    n = len(procs)
    remaining = {p.pid: p.burst_time for p in procs}
    completion = {}
    queue = []
    time = 0
    i = 0

    while i < n and procs[i].arrival_time <= time:
        queue.append(procs[i])
        i += 1
    if not queue and i < n:
        time = procs[i].arrival_time
        while i < n and procs[i].arrival_time <= time:
            queue.append(procs[i])
            i += 1

    while queue:
        p = queue.pop(0)
        run = min(quantum, remaining[p.pid])
        start = time
        time += run
        remaining[p.pid] -= run
        if (result.gantt and result.gantt[-1]["pid"] == p.pid
                and result.gantt[-1]["end"] == start):
            result.gantt[-1]["end"] = time
        else:
            result.gantt.append({"start": start, "end": time, "pid": p.pid})
        while i < n and procs[i].arrival_time <= time:
            queue.append(procs[i])
            i += 1
        if remaining[p.pid] > 0:
            queue.append(p)
        else:
            completion[p.pid] = time
        if not queue and i < n:
            time = procs[i].arrival_time
            while i < n and procs[i].arrival_time <= time:
                queue.append(procs[i])
                i += 1

    for p in sorted(procs, key=lambda p: p.pid):
        c = completion[p.pid]
        turnaround = c - p.arrival_time
        waiting = turnaround - p.burst_time
        result.add_detail(p.pid, p.arrival_time, p.burst_time,
                          waiting, turnaround, c)
    return result

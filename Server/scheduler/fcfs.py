from .result import Result


def fcfs(processes):
    result = Result("FCFS")
    order = sorted(processes, key=lambda p: (p.arrival_time, p.pid))
    time = 0
    completion = {}
    for p in order:
        if time < p.arrival_time:
            time = p.arrival_time
        start = time
        time += p.burst_time
        completion[p.pid] = time
        result.gantt.append({"start": start, "end": time, "pid": p.pid})
    for p in sorted(processes, key=lambda p: p.pid):
        c = completion[p.pid]
        turnaround = c - p.arrival_time
        waiting = turnaround - p.burst_time
        result.add_detail(p.pid, p.arrival_time, p.burst_time,
                          waiting, turnaround, c)
    return result

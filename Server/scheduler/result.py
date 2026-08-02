class Result:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.details = []
        self.gantt = []

    def add_detail(self, pid, arrival_time, burst_time,
                   waiting_time, turnaround_time, completion_time):
        self.details.append({
            "pid": pid,
            "arrival_time": arrival_time,
            "burst_time": burst_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
            "completion_time": completion_time,
        })

    def avg_waiting_time(self):
        if not self.details:
            return 0.0
        return sum(d["waiting_time"] for d in self.details) / len(self.details)

    def avg_turnaround_time(self):
        if not self.details:
            return 0.0
        return sum(d["turnaround_time"] for d in self.details) / len(self.details)

    def to_dict(self):
        return {
            "algorithm": self.algorithm,
            "details": self.details,
            "avg_waiting_time": round(self.avg_waiting_time(), 2),
            "avg_turnaround_time": round(self.avg_turnaround_time(), 2),
            "gantt": self.gantt,
        }

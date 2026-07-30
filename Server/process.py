"""
Process class
Only data structure for processes.
"""

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority, client_id):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.client_id = client_id

        # used later by Scheduler
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None

    def reset(self):
        self.remaining_time = self.burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None

    def to_dict(self):
        return {
            "pid": self.pid,
            "arrival_time": self.arrival_time,
            "burst_time": self.burst_time,
            "priority": self.priority,
            "client_id": self.client_id,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            pid=int(d["pid"]),
            arrival_time=int(d["arrival_time"]),
            burst_time=int(d["burst_time"]),
            priority=int(d["priority"]),
            client_id=str(d["client_id"]),
        )

    def __repr__(self):
        return (f"P{self.pid}(arr={self.arrival_time}, burst={self.burst_time}, "
                f"prio={self.priority}, client={self.client_id})")

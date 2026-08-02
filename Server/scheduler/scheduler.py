from .fcfs import fcfs
from .sjf import sjf
from .priority import priority
from .round_robin import round_robin

QUANTUM = 2


class Scheduler:
    def run_all(self, processes):
        return {
            "FCFS": fcfs(processes).to_dict(),
            "SJF (Preemptive)": sjf(processes).to_dict(),
            "Priority (Non-Preemptive)": priority(processes).to_dict(),
            "Round Robin (q=2)": round_robin(processes, QUANTUM).to_dict(),
        }

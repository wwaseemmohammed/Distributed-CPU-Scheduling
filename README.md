# Distributed CPU Scheduling

## Goal
Client generates processes and sends them to the server.
Server runs scheduling on those processes.

## Connection model
- New connection -> new thread
- Same connection, multiple process sends -> same thread, same queue
- Client disconnects -> that thread ends

## This part includes
- TCP Client + Server
- Process class
- One thread per connection
- Call Scheduler (if provided)
- Display results (and Gantt if scheduler returns it)

## Folder structure
```
Distributed-CPU-Scheduling/
├── Client/
│   ├── client.py
│   └── __init__.py
├── Server/
│   ├── server.py
│   ├── client_handler.py
│   ├── process.py
│   ├── config.py
│   ├── network_utils.py
│   └── __init__.py
├── README.md
```

## How to run
```
# Terminal 1
cd Server
python server.py

# Terminal 2
cd Client
python client.py
```

## Steps
1. Start server
2. Start client (opens a thread on server)
3. Option 1 -> send processes (can repeat; all stay on same thread)
4. Option 2 -> run scheduling on those processes
5. Option 6 -> disconnect (thread ends)

## Scheduler (other part)
Place `Server/scheduler.py`:
```python
class Scheduler:
    def run_all(self, processes):
        # return results for FCFS, SJF_Preemptive,
        # Priority_NonPreemptive, RoundRobin_q2
```

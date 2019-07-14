import psutil
pids = psutil.pids()
for pid in pids:
    p = psutil.Process(pid)
    print(p.name())
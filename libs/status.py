import psutil
import json
import datetime

def cpu_temperature():
    return psutil.sensors_temperatures()['cpu-thermal'][0].current

def disk_space():
    st = psutil.disk_usage(".")
    return st.free, st.total

def cpu_load() -> int:
    return int(psutil.cpu_percent())

def ram_usage() -> int:
    return int(psutil.virtual_memory().percent)

def uptime():
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")


def status_all(): 
    health = {'Uptime': uptime(),'CPUTemp': cpu_temperature(), 'CPULoad': cpu_load(), "DiskFree": disk_space()[0], "DiskTotal": disk_space()[1], "RAMUse": ram_usage()}
    print(health) 
    return health

if __name__ == '__main__':
    status_all()

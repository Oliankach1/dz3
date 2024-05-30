import psutil
from functools import wraps
import json

file = open('result', 'w')

def param_dec(par):
    def decorator0(func):
        @wraps(func)
        def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            with open('result', 'a+') as file:
                file.write(str(res) + '\n')
            with open(par , 'a+' ) as file:
                json.dump (res, file)
        
            return res
        return inner
    return decorator0

@param_dec('getcpu.json')
def get_cpu():
    load_bars = []
    cppc = psutil.cpu_percent(interval=1, percpu=True)
    for core, usage in enumerate(cppc):
        load_bar = "|" + "|" * int(usage / 10)
        load_bars.append(f"CORE{core}: {usage}% {load_bar}")
    return load_bars

@param_dec('getdisk.json')
def get_disk():
    du = psutil.disk_usage('/')
    dp = du.percent
    dps = f'disk usage={dp}%'
    return [dps]

@param_dec('getmem.json')
def get_mem():
    memory = psutil.virtual_memory()
    mp = memory.percent
    mps = f'memory usage={mp}%'
    return [mps]


def tb1():
    cpuinf = get_cpu()
    diskinf = get_disk()
    meminf = get_mem()
    headers = ['cpu', 'disk', 'memory']
    print('|{:^30}| |{:^20}| |{:^20}| '.format(*headers))
    print("-" * 78)
    for i in range(len(cpuinf)):
        print(f'{cpuinf[i]:<30}      {diskinf[0]:<20}   {meminf[0]:<20}')

@param_dec('getproc.json')
def get_processes():
    running_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'][:25]
            user = proc.info['username'] if proc.info['username'] else "N/A"
            memory_usage = proc.info['memory_percent']
            process_info = {'PID': pid, 'Name': name, 'User': user, 'Memory Usage (%)': memory_usage}
            running_processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return running_processes


def tasks_table():
    processes = get_processes()
    print("{:<8} {:<25} {:<15} {:<15}".format('PID', 'Name', 'User', 'Memory Usage (%)'))
    print("-" * 65)
    for process in processes:
        print("{:<8} {:<25} {:<15} {:<15.2f}".format(
            process['PID'], process['Name'], process['User'], process['Memory Usage (%)']))
    return 




def main():
    tb1()
    tasks_table()

if __name__ == '__main__':
    main()

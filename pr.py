import psutil
from functools import wraps
file= open('result', 'w')
def decorator0(func):
    @wraps(func)
    def inner():
        res= func()
        
        file = open('result', 'a+')
        for item in func():
            file.write ((item) + '\n')
            file.close
        return res
        
    return inner




@decorator0
def get_cpu():
    load_bars = []
    cppc= psutil.cpu_percent(interval=1, percpu=True)
    for core, usage in enumerate(cppc):
        load_bar = "|" + "|" * int(usage)
        load_bars.append(f" CORE{core}: {usage}% {load_bar}")    
    return (load_bars)


@decorator0
def get_disk():
    du= psutil.disk_usage('/')
    dp = du.percent
    dps = str('disk usage='f'{dp}%')
    dpst = [dps]
    return (dpst)

@decorator0
def get_mem():
    memory = psutil.virtual_memory()
    mp = memory.percent
    mps = str( 'memory usage='f'{mp}%')
    mpst = [mps]
    return (mpst)





def tb1():
    cpuinf = str (get_cpu())
    diskinf = str (get_disk())
    meminf = str (get_mem())
    headers = ['cpu', 'disk', 'memory']
    data1 = [cpuinf, diskinf, meminf]
    print ('|{:^30}| |{:^20}| |{:^20}| '.format(*headers))
    print("-" * 78) 
    for line in cpuinf:
        print (f'{line:<30}      {diskinf:<20}   {meminf:<20}')


@decorator0
def get_processes():
    running_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'][:25] 
            user = proc.info['username'] if proc.info['username'] else "N/A"
            memory_usage = proc.info['memory_percent']
            
            process_info = {'PID': pid, 'Name': name, 'User': user, 'Memory Usage (%)': memory_usage}
            process_inf = str (process_info)
            running_processes.append(process_inf)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return (running_processes)

def tasks_table():
    processes = get_processes()
    print("{:<8} {:<25} {:<15} {:<15}".format('PID', 'Name', 'User', 'Memory Usage (%)'))
    print("-" * 65) 
    for process in processes:
        print("{:<8} {:<25} {:<15} {:<15.2f}".format(process[0], process[1], process[2], process[3]))


decorator0(get_cpu())
decorator0(get_disk())
decorator0(get_mem())
decorator0(get_processes())
def main():
    tbc = tb1()
    tb2 = tasks_table()
    print (tbc, tb2)


if __name__ == '__main__':
    main()




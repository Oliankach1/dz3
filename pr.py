import psutil
def get_cpu():
    load_bars = []
    cppc= psutil.cpu_percent(interval=1, percpu=True)
    for core, usage in enumerate(cppc):
        load_bar = "|" + "|" * int(usage)
        load_bars.append(f" CORE{core}: {usage}% {load_bar}")
    return (load_bars)
def get_disk():
    du= psutil.disk_usage('/')
    dp = du.percent
    dps = str(f'{dp}%')
    return (dps)
def get_mem():
    memory = psutil.virtual_memory()
    mp = memory.percent
    mps = str(f'{mp}%')
    return (mps)
def tb1():
    cpuinf = get_cpu()
    diskinf = get_disk()
    meminf = get_mem()
    headers = ['cpu', 'disk', 'memory']
    data1 = [cpuinf, diskinf, meminf]
    print ('|{:^30}| |{:^20}| |{:^20}| '.format(*headers))
    print("-" * 78) 
    for loadi in cpuinf:
        print (f'{loadi:<30}      {diskinf:<20}   {meminf:<20}')




def tasks_table():
    
    print("{:<8} {:<25} {:<15} {:<15}".format('PID', 'Name', 'User', 'Memory Usage (%)'))
    print("-" * 65) 

    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'][:23]  
            user = proc.info['username'][:13] if proc.info['username'] else "N/A"  
            memory_usage = proc.info['memory_percent']
            
            print("{:<8} {:<25} {:<15} {:<15.2f}".format(pid, name, user, memory_usage))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass





def main():
    tbc = tb1()
    tb2 = tasks_table()
    print (tbc, tb2)


if __name__ == '__main__':
    main()
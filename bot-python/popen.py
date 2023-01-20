"""
import subprocess

count = '2'
ping = []
p1 = subprocess.run(['ping', '-c', count, '8.8.8.8'], capture_output=True)
split = str(p1.stdout).split('\\n')
for i in range(1, 1 + int(count)):
    time = split[i].split(" ")
    latency = time[6].replace("time=", "")
    ping.append(float(latency))
print(ping)

"""
import multiprocessing
import threading
import time
import pandas as pd
import paramiko

dataset = '20host.csv'

df = pd.read_csv(dataset)
listime = [[]]
j = 0
index = 0
for i in range(len(df)):
    initial = df.values[j][10]
    start = df.values[i][10]
    if start == initial:
        listime[index].append(i)
    else:
        listime.append([])
        j = i
        index += 1
        listime[index].append(i)

# Creating a list of threads
thread_list = []


def generate(i):
    df = pd.read_csv(dataset)
    ip = str(df.values[i][2]).split(".")
    last_digit = int(ip[3]) + 1
    docker_ip = f"172.17.0.{last_digit}"
    interface = f"h{int(ip[3])}-eth0"
    print("SSH into: " + str(docker_ip))

    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
    p.connect(docker_ip, port=22, username="root", password="root")

    srcip = df.values[i][2]
    dstip = df.values[i][3]
    smac = df.values[i][0]
    dmac = df.values[i][1]
    count = df.values[i][8]
    protocol = df.values[i][6]
    
    payload = ""
    for i in range(800):
        payload = payload + "A" 

    interval = 1. / 10
    pps = 50
    mbits = 0.5

    #stdin, stdout, stderr = p.exec_command(f"python3 /bot/traffic.py -s {srcip} -d {dstip} -smac {smac} -dmac "
    #                                       f"{dmac} -c {count} -if {interface} -p {protocol} -i {interval} -py {payload}")

    stdin, stdout, stderr = p.exec_command(f"python3 /bot/traffic1.py -s {srcip} -d {dstip} -smac {smac} -dmac "
                                          f"{dmac} -c {count} -if {interface} -p {protocol} -pps {pps} -mbits {mbits} -py {payload}")

    success = stdout.readlines()
    success = "".join(success)
    print(success)
    print()
    error = stderr.readlines()
    error = "".join(error)
    print(error)


if __name__ == '__main__':
    pro = []
    for j in range(len(listime)):
        inputs = listime[j]
        processes = [multiprocessing.Process(target=generate, args=(i,)) for i in inputs]
        [p.start() for p in processes]
        [pro.append(p) for p in processes]
        time.sleep(11)
    for p in pro:
        p.join()

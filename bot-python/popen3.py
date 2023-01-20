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
from random import randint

import pandas as pd
import paramiko

df = pd.read_csv('bot-dataset-test3.csv')
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
    df = pd.read_csv("bot-dataset-test3.csv")

    # The src ip (Client)
    ip1 = str(df.values[i][2]).split(".")
    last_digit1 = int(ip1[3]) + 1
    docker_ip1 = f"172.17.0.{last_digit1}"
    print("SSH into: " + str(docker_ip1))

    # The dst ip (Server)
    ip2 = str(df.values[i][3]).split(".")
    last_digit2 = int(ip2[3]) + 1
    docker_ip2 = f"172.17.0.{last_digit2}"
    print("SSH into: " + str(docker_ip2))

    p1 = paramiko.SSHClient()
    p1.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
    p1.connect(docker_ip1, port=22, username="root", password="root")

    p2 = paramiko.SSHClient()
    p2.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
    p2.connect(docker_ip2, port=22, username="root", password="root")

    dstip = df.values[i][3]
    port = df.values[i][4]
    protocol = df.values[i][6]
    duration = int(df.values[i][12])

    value = randint(5000, 6000)

    if duration > 60:
        duration = 60*1000
    if duration == 0:
        duration = 1*1000

    if protocol == 6:
        stdin2, stdout2, stderr2 = p2.exec_command(f"ITGRecv")
        stdin1, stdout1, stderr1 = p1.exec_command(f"ITGSend -a {dstip} -rp {value} -C 1000 -c 512 -t 15000 -T TCP -x recv_log_file")
        stdin3, stdout3, stderr3 = p1.exec_command(f"ITGDec recv_log_file")

    else:
        stdin2, stdout2, stderr2 = p2.exec_command(f"ITGRecv")
        stdin1, stdout1, stderr1 = p1.exec_command(f"ITGSend -a {dstip} -rp {value} -C 100 -c 512 -t 15000 -T UDP -x recv_log_file")
        stdin3, stdout3, stderr3 = p1.exec_command(f"ITGDec recv_log_file")

    success1 = stdout1.readlines()
    success1 = "".join(success1)
    print(success1)
    print("\n")
    success2 = stdout2.readlines()
    success2 = "".join(success2)
    print(success2)
    print("\n")
    success3 = stdout3.readlines()
    success3 = "".join(success3)
    print(success3)

    error1 = stderr1.readlines()
    error1 = "".join(error1)
    print(error1)
    print("\n")
    error2 = stderr2.readlines()
    error2 = "".join(error2)
    print(error2)
    print("\n")
    error3 = stderr3.readlines()
    error3 = "".join(error3)
    print(error3)


if __name__ == '__main__':
    pro = []
    for j in range(len(listime)):
        inputs = listime[j]
        processes = [multiprocessing.Process(target=generate, args=(i,)) for i in inputs]
        [p.start() for p in processes]
        [pro.append(p) for p in processes]
        time.sleep(5)
    for p in pro:
        p.join()

import multiprocessing
import threading
import time
import pandas as pd
import paramiko
'''
listime = [["172.17.0.2", "172.17.0.6"], ["172.17.0.3", "172.17.0.7"], ["172.17.0.4", "172.17.0.8"],
           ["172.17.0.5", "172.17.0.9"], ["172.17.0.6", "172.17.0.10"], ["172.17.0.7", "172.17.0.11"],
           ["172.17.0.8", "172.17.0.12"], ["172.17.0.9", "172.17.0.10"], ["172.17.0.10", "172.17.0.15"],
           ["172.17.0.11", "172.17.0.4"], ["172.17.0.12", "172.17.0.13"], ["172.17.0.14", "172.17.0.4"],
           ["172.17.0.15", "172.17.0.5"], ["172.17.0.16", "172.17.0.18"], ["172.17.0.17", "172.17.0.7"],
           ["172.17.0.20", "172.17.0.3"], ["172.17.0.14", "172.17.0.10"], ["172.17.0.16", "172.17.0.19"],
           ["172.17.0.13", "172.17.0.6"], ["172.17.0.4", "172.17.0.5"]]
'''
# listime = [["172.17.0.3", "172.17.0.5"]]
listime = [["172.17.0.2", "172.17.0.3"],["172.17.0.6", "172.17.0.7"],["172.17.0.11", "172.17.0.4"],["172.17.0.15", "172.17.0.5"],["172.17.0.8", "172.17.0.6"],["172.17.0.9", "172.17.0.7"],["172.17.0.10", "172.17.0.8"],["172.17.0.11", "172.17.0.9"]]

def generate(i):
    time.sleep(3)
    docker_ip1 = listime[i][0]
    docker_ip2 = listime[i][1]

    ip = docker_ip1.split(".")
    last_digit = int(ip[3]) - 1
    theip = f"10.0.0.{last_digit}"
    print(theip)

    p1 = paramiko.SSHClient()
    p1.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
    p1.connect(docker_ip1, port=22, username="root", password="root")

    p2 = paramiko.SSHClient()
    p2.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
    p2.connect(docker_ip2, port=22, username="root", password="root")

    stdin1, stdout1, stderr1 = p1.exec_command("iperf -s -u -p 5566 -i 1")
    stdin2, stdout2, stderr2 = p2.exec_command(f"iperf -c {theip} -u -b 5M -t 50 -p 5566")

    success = stdout2.readlines()
    success = "".join(success)
    print(success)

    print("\n")

    error = stderr2.readlines()
    error = "".join(error)
    print(error)


if __name__ == '__main__':
    pro = []
    # for j in range(len(listime)):
    inputs = len(listime)
    processes = [multiprocessing.Process(target=generate, args=(i,)) for i in range(inputs)]
    [p.start() for p in processes]
    [pro.append(p) for p in processes]
for p in pro:
    p.join()

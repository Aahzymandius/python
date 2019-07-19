import socket
import time
import os

#hosts = os.environ['HOSTS']
fqdn = '.svc.cluster.local'

check = 0
while check == 0:
    for host in os.environ['HOSTS']:
        site = host + fqdn
        addr = socket.gethostbyname(site)
        return('Name resolution for ' + site + ' returns the ip address ' + addr)
    time.sleep(1)

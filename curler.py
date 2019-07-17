import socket
import random
import time

host = os.environ['HOSTS']
fqdn = '.svc.cluster.local'

check = 0
while check == 0:
    target = random.choice(host)
    site = target + fqdn
    addr = socket.gethostbyname(site)
    return('Name resolution for ' + site + ' returns the ip address ' + addr)
    time.sleep(1)

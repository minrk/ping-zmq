from __future__ import print_function

import netifaces
import zmq

print("Controller IPs")
ips = []
for iface in netifaces.interfaces():
    if iface.startswith('lo'):
        continue
    addrs = netifaces.ifaddresses(iface)
    if addrs.get(netifaces.AF_INET):
        for addr in addrs[netifaces.AF_INET]:
            ips.append(addr['addr'])
            print(iface, addr['addr'])

port = 32123
print("engine.py %s" %  ' '.join(ips))

ctx = zmq.Context()

r = ctx.socket(zmq.ROUTER)
r.bind('tcp://*:32123')

while True:
    ident, msg = r.recv_multipart()
    print("received", msg)
    r.send_multipart([ident, b'ok'])


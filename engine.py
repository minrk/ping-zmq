from __future__ import print_function

import sys

import netifaces
import zmq

for iface in netifaces.interfaces():
    addrs = netifaces.ifaddresses(iface)
    if addrs.get(netifaces.AF_INET):
        for addr in addrs[netifaces.AF_INET]:
            print(iface, addr['addr'])

ctx = zmq.Context()
controller_port = 32123
controller_ips = sys.argv[1:]
assert controller_ips, "Must specify at least one controller IP"

for controller_ip in controller_ips:
    s = ctx.socket(zmq.DEALER)
    print("trying %s" % controller_ip)
    s.connect('tcp://%s:%i' % (controller_ip, controller_port))
    s.send(controller_ip.encode('ascii'))
    evt = s.poll(timeout=5000)
    if evt:
        reply = s.recv_multipart(zmq.NOBLOCK)
        print("%s works" % controller_ip)
    s.close(linger=0)

ctx.term()

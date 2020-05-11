#!/usr/bin/env python

import os
import sys
import subprocess
from scapy.all import *

nodeID = int(sys.argv[2])
aps = {'00:00:00:00:00:03': 50001, '00:00:00:00:00:04': 50002}
switches = {'00:00:00:00:00:05': 50003}
hosts = {'h1': ['10.0.0.2', '00:00:00:00:00:02']}
stations = {'sta1': ['10.0.0.1', '00:00:00:00:00:01']}


def handle_pkt(pkt):
    if pkt.addr2[-1:] == str(nodeID):
        for k, p in aps.items():
            if pkt.addr2 == k:
                ap_cmd = '/bin/bash -c \"simple_switch_CLI --thrift-port {} '.format(p)
                for s, a in stations.items():
                    table = '<<< \'table_add MyIngress.ipv4_lpm ipv4_forward {} => {} 1\'\"'.format(a[0], a[1])
                    cmd = ap_cmd + table
                    phys = subprocess.check_output(cmd, shell=True)
                    print(cmd)
                for h, a in hosts.items():
                    table = '<<< \'table_add MyIngress.ipv4_lpm ipv4_forward {} => {} 2\'\"'.format(a[0], a[1])
                    cmd = ap_cmd + table
                    phys = subprocess.check_output(cmd, shell=True)
                    print(cmd)

        for k, p in switches.items():
            switch_cmd = '/bin/bash -c \"simple_switch_CLI --thrift-port {} '.format(p)
            for h, a in hosts.items():
                table = '<<< \'table_add MyIngress.ipv4_lpm ipv4_forward {} => {} 3\'\"'.format(a[0], a[1])
                cmd = switch_cmd + table
                phys = subprocess.check_output(cmd, shell=True)
                print(cmd)
            for s, a in stations.items():
                port = 1
                if nodeID == 4:
                    port = 2
                table = '<<< \'table_add MyIngress.ipv4_lpm ipv4_forward {} => {} {}\'\"'.format(a[0], a[1], port)
                cmd = switch_cmd + table
                phys = subprocess.check_output(cmd, shell=True)
                print(cmd)
                if 'DUPLICATE' in str(phys):
                    switch_cmd = '/bin/bash -c \"simple_switch_CLI --thrift-port {} '.format(p)
                    table = '<<< \'table_modify MyIngress.ipv4_lpm ipv4_forward 1 {} {}\'\"'.format(a[1], port)
                    cmd = switch_cmd + table
                    phys = subprocess.check_output(cmd, shell=True)
                    print(cmd)


def main():
    iface = sys.argv[1]
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    sniff(iface=iface, lfilter=lambda x: x.haslayer(Dot11AssoResp) or x.haslayer(Dot11ReassoResp),
          prn=lambda x: handle_pkt(x))


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import sys
import subprocess
from scapy.all import *

nodeID = int(sys.argv[2])
SIP = [ip.strip() for ip in sys.argv[3].split(",")]
aps = {'00:00:00:00:00:03': 50002, '00:00:00:00:00:04': 50003}
switches = {'00:00:00:00:00:05': 50001}
hosts = {'h1': ['10.0.0.2', '00:00:00:00:00:02']}
stations = {'sta1': ['10.0.0.1', '00:00:00:00:00:01']}

def handle_pkt(pkt):
    if pkt.addr2[-1:] == str(nodeID):
        for index, (k, p) in enumerate(aps.items()):
            if pkt.addr2 == k:
                ap_cmd = '/bin/bash -c \"simple_switch_CLI --thrift-ip {} --thrift-port {} '.format(SIP[index], p)
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
            switch_cmd = '/bin/bash -c \"simple_switch_CLI --thrift-ip {} --thrift-port {} '.format(SIP[2], p)
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
                    switch_cmd = '/bin/bash -c \"simple_switch_CLI --thrift-ip {} --thrift-port {} '.format(SIP[2], p)
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

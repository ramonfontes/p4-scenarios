#!/usr/bin/python

import os

from containernet.net import Containernet
from containernet.node import DockerP4AP
from containernet.cli import CLI
from mininet.log import info, setLogLevel


def topology():
    'Create a network.'
    net = Containernet()

    info('*** Adding stations/hosts\n')
    sta1 = net.addStation('sta1', ip='10.0.1.1/24', mac="00:00:00:00:00:01")
    sta2 = net.addStation('sta2', ip='10.0.2.1/24', mac="00:00:00:00:00:02")

    path = os.path.dirname(os.getcwd())
    json_file = '/root/app.json'
    dimage = 'ramonfontes/bmv2:p4-scenarios'

    info('*** Adding P4APs\n')
    ap1 = net.addAccessPoint('ap1', cls=DockerP4AP, mac="00:00:00:00:00:03",
                             client_isolation=True, netcfg=True,
                             thriftport=50001, json=json_file,
                             dimage=dimage, cpu_shares=20,
                             environment={"DISPLAY": ":1"}, privileged=True,
                             volumes=[path + "/ip_routing/:/root",
                                      "/tmp/.X11-unix:/tmp/.X11-unix:rw"])

    net.configureWifiNodes()

    info('*** Creating links\n')
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    info('*** Starting network\n')
    net.start()
    net.staticArp()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
#!/usr/bin/python

import os

from containernet.net import Containernet
from containernet.node import DockerSta, DockerP4AP, DockerP4Switch
from containernet.cli import CLI
from mn_wifi.sixLoWPAN.link import LoWPAN
from mn_wifi.wmediumdConnector import interference
from mn_wifi.link import wmediumd
from mininet.log import info, setLogLevel
from mininet.term import makeTerm


def topology():
    'Create a network.'
    net = Containernet(link=wmediumd, wmediumd_mode=interference)

    dimage = 'ramonfontes/bmv2:p4-scenarios'
    path = os.path.dirname(os.getcwd())
    json_file = '/root/app.json'

    info('*** Adding APs/Switches\n')
    s1 = net.addSwitch('s1', cls=DockerP4Switch, mac="00:00:00:00:00:05",
                       netcfg=True, thriftport=50001, json=json_file,
                       dimage=dimage, cpu_shares=20,
                       environment={"DISPLAY": ":1"}, privileged=True,
                       volumes=[path + "/handover/:/root",
                                "/tmp/.X11-unix:/tmp/.X11-unix:rw"])
    ap1 = net.addAccessPoint('ap1', cls=DockerP4AP, mac="00:00:00:00:00:03",
                             ssid='handover', channel=1, position='40,40,0',
                             passwd='123456789a', encrypt='wpa2',
                             bssid_list=[['00:00:00:00:00:04']],
                             ieee80211r=True, mobility_domain='a1b2',
                             netcfg=True, thriftport=50002, json=json_file,
                             dimage=dimage, cpu_shares=20,
                             environment={"DISPLAY": ":1"}, privileged=True,
                             volumes=[path + "/handover/:/root",
                                      "/tmp/.X11-unix:/tmp/.X11-unix:rw"])
    ap2 = net.addAccessPoint('ap2', cls=DockerP4AP, mac="00:00:00:00:00:04",
                             ssid='handover', channel=6, position='80,40,0',
                             passwd='123456789a', encrypt='wpa2',
                             bssid_list=[['00:00:00:00:00:03']],
                             ieee80211r=True, mobility_domain='a1b2',
                             netcfg=True, thriftport=50003, json=json_file,
                             dimage=dimage, cpu_shares=20,
                             environment={"DISPLAY": ":1"}, privileged=True,
                             volumes=[path + "/handover/:/root",
                                      "/tmp/.X11-unix:/tmp/.X11-unix:rw"])

    info('*** Adding Stations\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1', mac="00:00:00:00:00:01",
                          bgscan_threshold=-70, s_inverval=1, l_interval=2,
                          bgscan_module="simple")
    h1 = net.addHost('h1', ip='10.0.0.2', mac="00:00:00:00:00:02")

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    net.configureWifiNodes()

    info("*** Adding links\n")
    net.addLink(s1, ap1)
    net.addLink(s1, ap2)
    net.addLink(s1, h1)

    net.plotGraph(max_x=200, max_y=200)

    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,30,0')
    net.mobility(sta1, 'stop', time=59, position='110,30,0')
    net.stopMobility(time=60)

    info('*** Starting network\n')
    net.start()
    net.staticArp()

    ap1.cmd('iw dev ap1-wlan1 interface add mon1 type monitor')
    ap2.cmd('iw dev ap2-wlan1 interface add mon2 type monitor')
    ap1.cmd('ip link set mon1 up')
    ap2.cmd('ip link set mon2 up')

    makeTerm(ap1, cmd="bash -c 'python /root/controller.py "
                      "mon1 3 {};'".format(",".join([ap1.sip, ap2.sip, s1.sip])))
    makeTerm(ap2, cmd="bash -c 'python /root/controller.py "
                      "mon2 4 {};'".format(",".join([ap1.sip, ap2.sip, s1.sip])))

    info('*** Running CLI\n')
    CLI(net)

    os.system('pkill -f -9 \"xterm\"')

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()


## Network Topology

The provided diagram represents a P4-enabled Wi-Fi network topology with one access points (AP) and two stations (hosts). The AP acts as P4 switch running simple_switch_grpc, allowing for programmable data plane behavior. The topology simulates a basic wireless network where AP forward traffic between stations based on P4 rules.

![](https://raw.githubusercontent.com/ramonfontes/p4-scenarios/45b1ff4e544820aad4b5bdc763cfdb09ab05103f/imgs/handover.png)

## Running the Scenario

The command below initializes the network using Containernet.
```
sudo python topology.py 
*** Adding stations/hosts
*** Adding P4APs
*** Creating links
*** Starting network
*** Starting controller(s)

*** Starting L2 nodes
ap1 ...⚡️ simple_switch_grpc @ 9718 thrift @ 50001

*** Running CLI
*** Starting CLI:
containernet>
```

To verify connectivity between stations, we attempt a ping from `sta1` to `sta2`:
```
sta1 ping -c1 sta2
ping: connect: Network is unreachable
```

Next, we configure the P4 switch by adding forwarding rules to the MyIngress.ipv4_lpm table:
```
ap1 simple_switch_CLI --thrift-port 50001 <<< "table_add MyIngress.ipv4_lpm ipv4_forward 10.0.1.1/32 => 00:00:00:00:00:01 1"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: Adding entry to lpm match table MyIngress.ipv4_lpm
match key:           LPM-0a:00:01:01/32
action:              ipv4_forward
runtime data:        00:00:00:00:00:01	00:01
Entry has been added with handle 0
RuntimeCmd:

ap1 simple_switch_CLI --thrift-port 50001 <<< "table_add MyIngress.ipv4_lpm ipv4_forward 10.0.2.1/32 => 00:00:00:00:00:02 1"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: Adding entry to lpm match table MyIngress.ipv4_lpm
match key:           LPM-0a:00:02:01/32
action:              ipv4_forward
runtime data:        00:00:00:00:00:02	00:01
Entry has been added with handle 1
RuntimeCmd:
```

We then set up default routes for `sta1` and `sta2`:
```
sta1 route add default gw 10.0.1.254 dev sta1-wlan0
sta2 route add default gw 10.0.2.254 dev sta2-wlan0
```


Testing connectivity again, the ping fails due to an unreachable destination:
```
sta1 ping -c1 sta2
PING 10.0.2.1 (10.0.2.1) 56(84) bytes of data.
From 10.0.1.1 icmp_seq=1 Destination Host Unreachable

--- 10.0.2.1 ping statistics ---
1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms
```

To resolve this, we manually set ARP entries:
```
sta1 arp -i sta1-wlan0 -s 10.0.1.254 00:00:00:00:00:03
sta2 arp -i sta2-wlan0 -s 10.0.2.254 00:00:00:00:00:03
```

Finally, after updating the ARP table, the ping succeeds:
```
sta1 ping -c1 sta2
PING 10.0.2.1 (10.0.2.1) 56(84) bytes of data.
64 bytes from 10.0.2.1: icmp_seq=1 ttl=63 time=3.84 ms

--- 10.0.2.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 3.842/3.842/3.842/0.000 ms
```

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

### Checking the P4 Table

To inspect the current table entries in MyIngress.ipv4_lpm, use:
```
ap1 simple_switch_CLI --thrift-port 50001 <<< "show_tables"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: MyIngress.ipv4_lpm             [implementation=None, mk=ipv4.dstAddr(lpm, 32)]
RuntimeCmd:
```

To dump the current IPv4 forwarding table:
```
ap1 simple_switch_CLI --thrift-port 50001 <<< "table_dump MyIngress.ipv4_lpm"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: ==========
TABLE ENTRIES
==========
Dumping default entry
Action entry: MyIngress.drop - 
==========
RuntimeCmd:
```

### Adding Entries to the P4 Table

To add forwarding rules for specific IP addresses:

```
ap1 simple_switch_CLI --thrift-port 50001 <<< "table_add MyIngress.ipv4_lpm ipv4_forward 10.0.0.1/32 => 00:00:00:00:00:01 1"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: Adding entry to lpm match table MyIngress.ipv4_lpm
match key:           LPM-0a:00:00:01/32
action:              ipv4_forward
runtime data:        00:00:00:00:00:01	00:01
Entry has been added with handle 0
RuntimeCmd:

ap1 simple_switch_CLI --thrift-port 50001 <<< "table_add MyIngress.ipv4_lpm ipv4_forward 10.0.0.2/32 => 00:00:00:00:00:02 1"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: Adding entry to lpm match table MyIngress.ipv4_lpm
match key:           LPM-0a:00:00:02/32
action:              ipv4_forward
runtime data:        00:00:00:00:00:02	00:01
Entry has been added with handle 1
RuntimeCmd:
```

### Verifying the Table Entries

```
ap1 simple_switch_CLI --thrift-port 50001 <<< "table_dump MyIngress.ipv4_lpm"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: ==========
TABLE ENTRIES
**********
Dumping entry 0x0
Match key:
* ipv4.dstAddr        : LPM       0a000001/32
Action entry: MyIngress.ipv4_forward - 01, 01
**********
Dumping entry 0x1
Match key:
* ipv4.dstAddr        : LPM       0a000002/32
Action entry: MyIngress.ipv4_forward - 02, 01
==========
Dumping default entry
Action entry: MyIngress.drop - 
==========
RuntimeCmd:
```

### Testing Connectivity

To test if `sta1` can reach `sta2`, run a ping command:

```
sta1 ping -c1 sta2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=63 time=4.34 ms

--- 10.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 4.341/4.341/4.341/0.000 ms
```
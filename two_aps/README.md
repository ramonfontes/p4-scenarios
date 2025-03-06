
## Network Topology

The provided diagram represents a P4-enabled Wi-Fi network topology with two access points (APs) and two stations (hosts). The APs act as P4 switches running simple_switch_grpc, allowing for programmable data plane behavior. The topology simulates a basic wireless network where APs forward traffic between stations based on P4 rules.

![](https://raw.githubusercontent.com/ramonfontes/p4-scenarios/45b1ff4e544820aad4b5bdc763cfdb09ab05103f/imgs/two-aps.png)

## Running the Scenario

The command below initializes the network using Containernet.
```
sudo python topology.py 
*** Adding stations  
*** Adding P4APs  
*** Creating links  
 *** Starting networkh2 up:   
*** Starting controller(s)  

*** Starting L2 nodes  
ap1 ...⚡️ simple_switch_grpc @ 15924 thrift @ 50001  
ap2 ...⚡️ simple_switch_grpc @ 15968 thrift @ 50002  

*** Running CLI  
*** Starting CLI:  
containernet>
```

### Initial Ping Attempt (Failure)

`sta1` attempts to ping `sta2`, but the packets are not forwarded.
Reason for failure: No forwarding rules are configured in the P4 tables, meaning packets do not reach their destination.
```
containernet> sta1 ping -c1 sta2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
^C
--- 10.0.0.2 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
```
### Configuring Forwarding Rules on ap1

The command below adds a match-action entry to the P4 forwarding table on `ap1`.

- Match Condition: If a packet is destined to 10.0.0.1, it is forwarded to MAC address 00:00:00:00:00:01 via port 1.
- Effect: This allows `ap1` to handle packets directed to 10.0.0.1.

```
containernet> ap1 simple_switch_CLI --thrift-port 50001 <<< "table_add MyIngress.ipv4_lpm ipv4_forward 10.0.0.1 => 00:00:00:00:00:01 1"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: Adding entry to exact match table MyIngress.ipv4_lpm
match key:           EXACT-0a:00:00:01
action:              ipv4_forward
runtime data:        00:00:00:00:00:01	00:01
Entry has been added with handle 0
RuntimeCmd: 
```

### Configuring Forwarding Rules on ap2

Similar to the previous step, but applied to `ap2`.

- Effect: `ap2` forwards packets destined to 10.0.0.2 to MAC address 00:00:00:00:00:02 via port 1.

```
containernet> ap2 simple_switch_CLI --thrift-port 50002 <<< "table_add MyIngress.ipv4_lpm ipv4_forward 10.0.0.2 => 00:00:00:00:00:02 1"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: Adding entry to exact match table MyIngress.ipv4_lpm
match key:           EXACT-0a:00:00:02
action:              ipv4_forward
runtime data:        00:00:00:00:00:02	00:01
Entry has been added with handle 0
RuntimeCmd: 
```

### Configuring Bidirectional Forwarding on ap1

The command below adds an additional forwarding rule to `ap1`, ensuring it forwards packets to 10.0.0.2 via port 2.
- Effect: Enables bidirectional communication from `sta1` to `sta2` through `ap1`.
```
containernet> ap1 simple_switch_CLI --thrift-port 50001 <<< "table_add MyIngress.ipv4_lpm ipv4_forward 10.0.0.2 => 00:00:00:00:00:02 2"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: Adding entry to exact match table MyIngress.ipv4_lpm
match key:           EXACT-0a:00:00:02
action:              ipv4_forward
runtime data:        00:00:00:00:00:02	00:02
Entry has been added with handle 1
RuntimeCmd: 
```
### Configuring Bidirectional Forwarding on ap2

Similarly, the rule below allows `ap2` to forward packets destined for 10.0.0.1 via port 2.
- Effect: Ensures proper routing in both directions.
```
containernet> ap2 simple_switch_CLI --thrift-port 50002 <<< "table_add MyIngress.ipv4_lpm ipv4_forward 10.0.0.1 => 00:00:00:00:00:01 2"
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: Adding entry to exact match table MyIngress.ipv4_lpm
match key:           EXACT-0a:00:00:01
action:              ipv4_forward
runtime data:        00:00:00:00:00:01	00:02
Entry has been added with handle 1
RuntimeCmd: 
```

### Successful Ping Test

`sta1` successfully pings `sta2`, confirming that packets are now correctly routed through the P4-enabled APs.
- Round-trip time (RTT): 5.93 ms, indicating efficient packet forwarding.


```
containernet> sta1 ping -c1 sta2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=62 time=5.93 ms

--- 10.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 5.928/5.928/5.928/0.000 ms
```
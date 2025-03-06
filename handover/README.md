
## Network Topology

The provided diagram represents a P4-enabled Wi-Fi network topology with two access points (APs) and two stations (hosts). The APs act as P4 switches running simple_switch_grpc, allowing for programmable data plane behavior. The topology simulates a basic wireless network where APs forward traffic between stations based on P4 rules.

![](https://raw.githubusercontent.com/ramonfontes/p4-scenarios/45b1ff4e544820aad4b5bdc763cfdb09ab05103f/imgs/handover.png)

## Running the Scenario

The command below initializes the network using Containernet.
```
sudo python topology.py 
*** Adding APs/Switches
*** Adding Stations
*** Configuring propagation model
*** Connecting to wmediumd server /var/run/wmediumd.sock
*** Adding links
 *** Starting network3 up:  
*** Starting controller(s)

*** Starting L2 nodes
s1 ..⚡️ simple_switch_grpc @ 7390 thrift @ 50001
ap1 ..⚡️ simple_switch_grpc @ 7434 thrift @ 50002
ap2 ..⚡️ simple_switch_grpc @ 7477 thrift @ 50003

*** Running CLI
*** Starting CLI:
containernet>
```

To verify connectivity, a ping test was conducted from `sta1` to `h1`, producing the following results:
```
sta1 ping h1
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=62 time=1.88 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=62 time=1.54 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=62 time=1.84 ms
64 bytes from 10.0.0.2: icmp_seq=5 ttl=62 time=2.08 ms
64 bytes from 10.0.0.2: icmp_seq=6 ttl=62 time=2.07 ms
64 bytes from 10.0.0.2: icmp_seq=7 ttl=62 time=2.12 ms
64 bytes from 10.0.0.2: icmp_seq=8 ttl=62 time=1.77 ms
64 bytes from 10.0.0.2: icmp_seq=9 ttl=62 time=2.18 ms
64 bytes from 10.0.0.2: icmp_seq=10 ttl=62 time=1.66 ms
64 bytes from 10.0.0.2: icmp_seq=11 ttl=62 time=1.58 ms
64 bytes from 10.0.0.2: icmp_seq=12 ttl=62 time=2.09 ms
64 bytes from 10.0.0.2: icmp_seq=13 ttl=62 time=2.15 ms
64 bytes from 10.0.0.2: icmp_seq=14 ttl=62 time=1.82 ms
64 bytes from 10.0.0.2: icmp_seq=15 ttl=62 time=1.42 ms
64 bytes from 10.0.0.2: icmp_seq=16 ttl=62 time=1.85 ms
64 bytes from 10.0.0.2: icmp_seq=17 ttl=62 time=1.80 ms
64 bytes from 10.0.0.2: icmp_seq=18 ttl=62 time=1.56 ms
64 bytes from 10.0.0.2: icmp_seq=19 ttl=62 time=5.47 ms
64 bytes from 10.0.0.2: icmp_seq=20 ttl=62 time=2.03 ms
64 bytes from 10.0.0.2: icmp_seq=21 ttl=62 time=1.67 ms
64 bytes from 10.0.0.2: icmp_seq=22 ttl=62 time=1.40 ms
64 bytes from 10.0.0.2: icmp_seq=23 ttl=62 time=2.39 ms
64 bytes from 10.0.0.2: icmp_seq=24 ttl=62 time=1.59 ms
64 bytes from 10.0.0.2: icmp_seq=25 ttl=62 time=2.36 ms
64 bytes from 10.0.0.2: icmp_seq=26 ttl=62 time=3.48 ms
64 bytes from 10.0.0.2: icmp_seq=27 ttl=62 time=4.43 ms
64 bytes from 10.0.0.2: icmp_seq=28 ttl=62 time=4.23 ms
64 bytes from 10.0.0.2: icmp_seq=29 ttl=62 time=4.52 ms
64 bytes from 10.0.0.2: icmp_seq=30 ttl=62 time=2.85 ms
64 bytes from 10.0.0.2: icmp_seq=31 ttl=62 time=4.63 ms
64 bytes from 10.0.0.2: icmp_seq=32 ttl=62 time=4.25 ms
64 bytes from 10.0.0.2: icmp_seq=33 ttl=62 time=1.98 ms
64 bytes from 10.0.0.2: icmp_seq=34 ttl=62 time=3.91 ms
64 bytes from 10.0.0.2: icmp_seq=35 ttl=62 time=3.21 ms
64 bytes from 10.0.0.2: icmp_seq=36 ttl=62 time=3.15 ms
64 bytes from 10.0.0.2: icmp_seq=37 ttl=62 time=4.75 ms
64 bytes from 10.0.0.2: icmp_seq=38 ttl=62 time=3.17 ms
64 bytes from 10.0.0.2: icmp_seq=39 ttl=62 time=2.67 ms
64 bytes from 10.0.0.2: icmp_seq=40 ttl=62 time=2.97 ms
64 bytes from 10.0.0.2: icmp_seq=41 ttl=62 time=2.42 ms
64 bytes from 10.0.0.2: icmp_seq=42 ttl=62 time=2.65 ms
64 bytes from 10.0.0.2: icmp_seq=43 ttl=62 time=1.87 ms
64 bytes from 10.0.0.2: icmp_seq=44 ttl=62 time=2.20 ms
64 bytes from 10.0.0.2: icmp_seq=45 ttl=62 time=2.14 ms
64 bytes from 10.0.0.2: icmp_seq=46 ttl=62 time=2.24 ms
64 bytes from 10.0.0.2: icmp_seq=47 ttl=62 time=1.89 ms
64 bytes from 10.0.0.2: icmp_seq=48 ttl=62 time=1.77 ms
64 bytes from 10.0.0.2: icmp_seq=49 ttl=62 time=4.46 ms
64 bytes from 10.0.0.2: icmp_seq=50 ttl=62 time=4.63 ms
```

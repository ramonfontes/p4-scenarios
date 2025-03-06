
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


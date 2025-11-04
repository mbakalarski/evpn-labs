#!/bin/bash

set -e

log_green() {
  echo
  echo -e "\033[32m${1}\033[0m"
}

kubectl cp leaf1_evpn.cfg leaf1:/leaf1_evpn.cfg
kubectl cp leaf2_evpn.cfg leaf2:/leaf2_evpn.cfg

kubectl exec leaf1 -- bash -c 'sr_cli --candidate-mode --commit-at-end < /leaf1_evpn.cfg'
kubectl exec leaf2 -- bash -c 'sr_cli --candidate-mode --commit-at-end < /leaf2_evpn.cfg'

log_green "## IBGP for EVPN"
kubectl exec -ti leaf1 -- sr_cli show network-instance default protocols bgp neighbor 10.0.0.2

log_green "## Tunnel/VXLAN interfaces"
kubectl exec -ti leaf1 -- sr_cli show tunnel-interface vxlan-interface brief
kubectl exec -ti leaf2 -- sr_cli show tunnel-interface vxlan-interface brief

log_green "## Configure MAC and IP addresses on the servers"
kubectl exec srv1 -- ip link set address 00:c1:ab:00:00:01 dev eth1
kubectl exec srv1 -- ip addr replace 192.168.0.1/24 dev eth1
kubectl exec srv2 -- ip link set address 00:c1:ab:00:00:02 dev eth1
kubectl exec srv2 -- ip addr replace 192.168.0.2/24 dev eth1

log_green "## Ping srv2 from srv1"
kubectl exec srv1 -- ping 192.168.0.2 -c1

log_green "## Show locally learned/learnt MACs in leaf1 and leaf2"
kubectl exec -ti leaf1 -- sr_cli show network-instance vrf-1 bridge-table mac-table all
kubectl exec -ti leaf2 -- sr_cli show network-instance vrf-1 bridge-table mac-table all

log_green "## EVPN in MAC-VRF / check RT/RD values"
kubectl exec -ti leaf1 -- sr_cli show network-instance vrf-1 protocols bgp-vpn bgp-instance 1
kubectl exec -ti leaf2 -- sr_cli show network-instance vrf-1 protocols bgp-vpn bgp-instance 1

log_green "## Ping srv2 from srv1"
kubectl exec srv1 -- ping 192.168.0.2 -c1

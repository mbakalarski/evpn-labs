#!/bin/bash

set -e

log_green() {
  echo
  echo -e "\033[32m${1}\033[0m"
}


kubectl cp spine1.cfg spine1:/spine1.cfg
kubectl cp leaf1.cfg leaf1:/leaf1.cfg
kubectl cp leaf2.cfg leaf2:/leaf2.cfg

kubectl exec spine1 -- bash -c 'sr_cli --candidate-mode --commit-at-end < /spine1.cfg'
kubectl exec leaf1 -- bash -c 'sr_cli --candidate-mode --commit-at-end < /leaf1.cfg'
kubectl exec leaf2 -- bash -c 'sr_cli --candidate-mode --commit-at-end < /leaf2.cfg'

log_green "# Verification:"

log_green "## LLDP neighbors"
kubectl exec spine1 -- sr_cli show system lldp neighbor

log_green "## Ping from spine1 to leaf1 and leaf2"
kubectl exec -ti spine1 -- sr_cli ping network-instance default 192.168.11.1 -c3
kubectl exec -ti spine1 -- sr_cli ping network-instance default 192.168.12.1 -c3

log_green "## BGP status"
kubectl exec -ti leaf1 -- sr_cli show network-instance default protocols bgp summary

log_green "## BGP neighbor status"
kubectl exec -ti spine1 -- sr_cli show network-instance default protocols bgp neighbor

log_green "## Received/Advertised routes"
kubectl exec -ti leaf1 -- sr_cli show network-instance default protocols bgp neighbor 192.168.11.2 advertised-routes ipv4
kubectl exec -ti leaf2 -- sr_cli show network-instance default protocols bgp neighbor 192.168.12.2 received-routes ipv4

log_green "## Route table"
kubectl exec -ti leaf1 -- sr_cli show network-instance default route-table ipv4-unicast summary

log_green "## Dataplane for VTEPs"
kubectl exec -ti leaf1 -- sr_cli ping -I 10.0.0.1 network-instance default 10.0.0.2 -c3

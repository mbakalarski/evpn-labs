#!/bin/bash

set -e

log_green() {
  echo
  echo -e "\033[32m${1}\033[0m"
}

log_green "EVPN IMET/RT3 routes"
kubectl exec -ti leaf1 -- sr_cli /show network-instance default protocols bgp neighbor 10.0.0.2

log_green "EVPN Type-3 routes summary"
kubectl exec -ti leaf1 -- sr_cli /show network-instance default protocols bgp routes evpn route-type 3 summary

log_green "EVPN Type-3 routes details"
kubectl exec -ti leaf1 -- sr_cli /show network-instance default protocols bgp routes evpn route-type 3 detail

log_green "BUM destinations in leaf1"
kubectl exec -ti leaf1 -- sr_cli /show tunnel-interface vxlan1 vxlan-interface 1 bridge-table multicast-destinations destination
#!/usr/bin/env python3
"""
example usage:
python yaml_to_mermaid.py topology.yaml -o topology_styled.mmd -d LR
"""

import yaml
import argparse
from pathlib import Path
from collections import defaultdict

def generate_mermaid_with_networks_as_invisible_nodes(yaml_file, direction="TD"):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    mermaid_code = f"graph {direction}\n"
    mermaid_code += "    %% Auto-generated network topology diagram (networks as invisible nodes)\n\n"

    network_links = defaultdict(list)
    node_types = {}

    # Collect node data and connections
    for node in data["topology"]["nodes"]:
        node_name = node["name"]
        node_type = node.get("type", "unknown")
        node_types[node_name] = node_type

        for iface in node.get("interfaces", []):
            net = iface["network"]
            network_links[net].append(node_name)

    # Node styles
    mermaid_code += "    classDef srlinux fill:#b3d9ff,stroke:#003366,stroke-width:2px;\n"
    mermaid_code += "    classDef linux fill:#b3ffb3,stroke:#006600,stroke-width:2px;\n"
    mermaid_code += "    classDef network fill:#ffffff,stroke:none,stroke-width:0px;\n\n"

    # Render connections via invisible network nodes
    for net, nodes in network_links.items():
        if len(nodes) < 2:
            continue  # Skip networks with only one connection
        # Chain nodes through the network
        # Example: nodeA --> net --> nodeB --> net --> nodeC
        first_node = nodes[0]
        mermaid_code += f"    {first_node} --> {net}\n"
        for other_node in nodes[1:]:
            mermaid_code += f"    {net} --> {other_node}\n"

    # Assign node styles
    for node, ntype in node_types.items():
        if ntype == "srlinux":
            mermaid_code += f"    class {node} srlinux;\n"
        elif ntype == "linux":
            mermaid_code += f"    class {node} linux;\n"

    for net in network_links.keys():
        mermaid_code += f"    class {net} network;\n"

    return mermaid_code


def main():
    parser = argparse.ArgumentParser(
        description="Convert network topology YAML into a GitHub-renderable Mermaid diagram with networks as invisible nodes."
    )
    parser.add_argument("input", help="Input YAML topology file")
    parser.add_argument(
        "-o", "--output", default="network_topology.mmd",
        help="Output Mermaid (.mmd) file name"
    )
    parser.add_argument(
        "-d", "--direction", choices=["TD", "LR", "BT", "RL"], default="TD",
        help="Diagram layout direction (TD=top-down, LR=left-right, BT=bottom-top, RL=right-left)"
    )

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"❌ Error: Input file '{input_path}' not found.")
        return

    mermaid_code = generate_mermaid_with_networks_as_invisible_nodes(input_path, args.direction)

    with open(output_path, "w") as f:
        f.write(mermaid_code)

    print(f"✅ Mermaid diagram saved to: {output_path}")
    print(f"📈 Layout direction: {args.direction}")


if __name__ == "__main__":
    main()

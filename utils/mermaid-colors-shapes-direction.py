#!/usr/bin/env python3
"""
example usage:
python yaml_to_mermaid.py topology.yaml -o topology_styled.mmd -d LR
"""

import yaml
import argparse
from pathlib import Path
from collections import defaultdict

def generate_mermaid_from_yaml(yaml_file, direction="TD"):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    mermaid_code = f"graph {direction}\n"
    mermaid_code += "    %% Auto-generated GitHub-compatible network topology diagram\n\n"

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

    # Categorize networks
    spine_leaf_networks = [n for n in network_links if n.startswith("s")]
    leaf_ce_networks = [n for n in network_links if n.startswith("l")]
    other_networks = [
        n for n in network_links if not (n.startswith("s") or n.startswith("l"))
    ]

    # Node styles
    mermaid_code += "    classDef srlinux fill:#b3d9ff,stroke:#003366,stroke-width:2px;\n"
    mermaid_code += "    classDef linux fill:#b3ffb3,stroke:#006600,stroke-width:2px;\n"
    mermaid_code += "    classDef network fill:#fff5b3,stroke:#b38f00,stroke-width:1px,shape:circle;\n\n"

    # Helper to render connections (without subgraphs per network)
    def render_connections(title, networks):
        code = f"    subgraph {title}\n"
        for net in networks:
            for node in network_links[net]:
                code += f"        {node} --> {net}\n"
        code += "    end\n\n"
        return code

    # Render groups
    if spine_leaf_networks:
        mermaid_code += render_connections("Spine_Leaf_Networks", spine_leaf_networks)
    if leaf_ce_networks:
        mermaid_code += render_connections("Leaf_CE_Networks", leaf_ce_networks)
    if other_networks:
        mermaid_code += render_connections("Other_Networks", other_networks)

    # Assign node styles
    mermaid_code += "    %% Assign node styles\n"
    for node, ntype in node_types.items():
        if ntype == "srlinux":
            mermaid_code += f"    class {node} srlinux;\n"
        elif ntype == "linux":
            mermaid_code += f"    class {node} linux;\n"
        else:
            mermaid_code += f"    class {node} network;\n"

    for net in network_links.keys():
        mermaid_code += f"    class {net} network;\n"

    return mermaid_code


def main():
    parser = argparse.ArgumentParser(
        description="Convert network topology YAML into a GitHub-renderable Mermaid diagram."
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

    mermaid_code = generate_mermaid_from_yaml(input_path, args.direction)

    with open(output_path, "w") as f:
        f.write(mermaid_code)

    print(f"✅ Mermaid diagram saved to: {output_path}")
    print(f"📈 Layout direction: {args.direction}")


if __name__ == "__main__":
    main()

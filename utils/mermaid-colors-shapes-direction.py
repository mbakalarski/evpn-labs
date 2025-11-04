#!/usr/bin/env python3
"""
example usage:
python3 ../utils/mermaid-colors-shapes-direction.py topology_evpn_mh.yaml -o mermaid4-TD.mmd -d TD

- Networks as edge labels → no extra nodes.
- Device nodes only → spine, leaf, CE.
- Dual-theme colors:
- srlinux → blue
- linux/CE → orange (ce)
- GitHub-compatible Mermaid.
- Configurable layout direction (TD, LR, BT, RL).
"""


import yaml
import argparse
from pathlib import Path

def generate_mermaid_with_edge_labels(yaml_file, direction="TD"):
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    mermaid_code = f"graph {direction}\n"
    mermaid_code += "    %% Auto-generated network topology diagram (networks as edge labels)\n\n"

    node_types = {}
    edges = []

    # Collect node types
    for node in data["topology"]["nodes"]:
        node_types[node["name"]] = node.get("type", "unknown")

    # Collect connections as edges (with network names as labels)
    for node in data["topology"]["nodes"]:
        src = node["name"]
        for iface in node.get("interfaces", []):
            net = iface["network"]
            # Connect to all other nodes on the same network
            for other_node in data["topology"]["nodes"]:
                dst = other_node["name"]
                if dst == src:
                    continue
                for other_iface in other_node.get("interfaces", []):
                    if other_iface["network"] == net:
                        # Avoid duplicate edges
                        if (dst, src, net) not in edges:
                            edges.append((src, dst, net))

    # Write edges
    for src, dst, net in edges:
        mermaid_code += f"    {src} -->|{net}| {dst}\n"

    # Node styles (light & dark theme friendly)
    mermaid_code += "\n    %% Node styles\n"
    mermaid_code += "    classDef srlinux fill:#4da6ff,stroke:#003366,stroke-width:2px,color:#000000;\n"
    mermaid_code += "    classDef linux fill:#66ff66,stroke:#006600,stroke-width:2px,color:#000000;\n"
    mermaid_code += "    classDef ce fill:#ffcc66,stroke:#994d00,stroke-width:2px,color:#000000;\n"

    # Assign node classes
    for node, ntype in node_types.items():
        if ntype == "srlinux":
            mermaid_code += f"    class {node} srlinux;\n"
        elif ntype == "linux":
            # Optional: assign CE style
            mermaid_code += f"    class {node} ce;\n"

    return mermaid_code

def main():
    parser = argparse.ArgumentParser(
        description="Convert network topology YAML into a GitHub Mermaid diagram with networks as edge labels."
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

    mermaid_code = generate_mermaid_with_edge_labels(input_path, args.direction)

    with open(output_path, "w") as f:
        f.write(mermaid_code)

    print(f"✅ Mermaid diagram saved to: {output_path}")
    print(f"📈 Layout direction: {args.direction}")


if __name__ == "__main__":
    main()

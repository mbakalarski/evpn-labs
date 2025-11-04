#!/usr/bin/env python3
"""
| Flag    | Description                    | Example                                         |
| ------- | ------------------------------ | ----------------------------------------------- |
| `-d TD` | Top-to-bottom layout (default) | `python yaml_to_mermaid.py topology.yaml`       |
| `-d LR` | Left-to-right layout           | `python yaml_to_mermaid.py topology.yaml -d LR` |
| `-d BT` | Bottom-to-top layout           | `python yaml_to_mermaid.py topology.yaml -d BT` |
| `-d RL` | Right-to-left layout           | `python yaml_to_mermaid.py topology.yaml -d RL` |

python yaml_to_mermaid.py topology.yaml -o topology_lr.mmd -d LR


"""

import yaml
import argparse
from pathlib import Path
from collections import defaultdict

def generate_mermaid_from_yaml(yaml_file, direction="TD"):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    mermaid_code = f"graph {direction}\n"
    mermaid_code += "    %% Auto-generated network topology diagram\n\n"

    network_links = defaultdict(list)

    # Collect node and interface data
    for node in data["topology"]["nodes"]:
        node_name = node["name"]
        for iface in node.get("interfaces", []):
            net = iface["network"]
            intf = iface["name"]
            network_links[net].append((node_name, intf))

    # Categorize networks by name
    spine_leaf_networks = [n for n in network_links if n.startswith("s")]
    leaf_ce_networks = [n for n in network_links if n.startswith("l")]
    other_networks = [
        n for n in network_links if not (n.startswith("s") or n.startswith("l"))
    ]

    # Helper: render subgraph for group of networks
    def render_subgraph(title, networks):
        code = f"    subgraph {title}\n"
        for net in networks:
            code += f"        subgraph {net}\n"
            for (node, iface) in network_links[net]:
                code += f"            {node} --> {net}\n"
            code += "        end\n"
        code += "    end\n\n"
        return code

    # Render each group
    if spine_leaf_networks:
        mermaid_code += render_subgraph("Spine_Leaf_Networks", spine_leaf_networks)
    if leaf_ce_networks:
        mermaid_code += render_subgraph("Leaf_CE_Networks", leaf_ce_networks)
    if other_networks:
        mermaid_code += render_subgraph("Other_Networks", other_networks)

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

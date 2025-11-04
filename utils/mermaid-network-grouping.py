#!/usr/bin/env python3
import yaml
import argparse
from pathlib import Path
from collections import defaultdict

def generate_mermaid_from_yaml(yaml_file):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    mermaid_code = "graph TD\n"
    mermaid_code += "    %% Auto-generated network topology\n"

    # Track which nodes connect to which networks
    network_links = defaultdict(list)

    # Collect node information
    for node in data["topology"]["nodes"]:
        node_name = node["name"]
        for iface in node.get("interfaces", []):
            net = iface["network"]
            intf = iface["name"]
            network_links[net].append((node_name, intf))

    # Categorize networks
    spine_leaf_networks = [n for n in network_links if n.startswith("s")]
    leaf_ce_networks = [n for n in network_links if n.startswith("l")]
    other_networks = [n for n in network_links if not (n.startswith("s") or n.startswith("l"))]

    # Helper to render subgraph
    def render_subgraph(name, networks):
        code = f"    subgraph {name}\n"
        for net in networks:
            code += f"        subgraph {net}\n"
            for (node, iface) in network_links[net]:
                code += f"            {node} --> {net}\n"
            code += "        end\n"
        code += "    end\n"
        return code

    # Render categorized networks
    if spine_leaf_networks:
        mermaid_code += render_subgraph("Spine_Leaf_Networks", spine_leaf_networks)
    if leaf_ce_networks:
        mermaid_code += render_subgraph("Leaf_CE_Networks", leaf_ce_networks)
    if other_networks:
        mermaid_code += render_subgraph("Other_Networks", other_networks)

    return mermaid_code


def main():
    parser = argparse.ArgumentParser(
        description="Convert network topology YAML to a grouped Mermaid diagram."
    )
    parser.add_argument("input", help="Input YAML topology file")
    parser.add_argument(
        "-o", "--output",
        help="Output Mermaid (.mmd) file name",
        default="network_topology.mmd"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"❌ Error: Input file '{input_path}' not found.")
        return

    mermaid_code = generate_mermaid_from_yaml(input_path)

    with open(output_path, "w") as f:
        f.write(mermaid_code)

    print(f"✅ Mermaid diagram saved to: {output_path}")


if __name__ == "__main__":
    main()

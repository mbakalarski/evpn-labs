#!/usr/bin/env python3
import yaml
import argparse
from pathlib import Path

def generate_mermaid_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    mermaid_code = "graph TD\n"

    # Collect nodes and networks
    nodes = {}

    for node in data['topology']['nodes']:
        node_name = node['name']
        nodes[node_name] = node_name

        for interface in node.get('interfaces', []):
            network = interface['network']
            if network not in nodes:
                nodes[network] = network
            mermaid_code += f"    {node_name} --> {network}\n"

    return mermaid_code


def main():
    parser = argparse.ArgumentParser(
        description="Convert custom network topology YAML to Mermaid diagram format."
    )
    parser.add_argument("input", help="Path to the input YAML topology file")
    parser.add_argument(
        "-o", "--output", help="Path to output Mermaid (.mmd) file", default="network_topology.mmd"
    )

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"❌ Error: Input file '{input_path}' not found.")
        return

    mermaid_code = generate_mermaid_from_yaml(input_path)

    with open(output_path, "w") as out:
        out.write(mermaid_code)

    print(f"✅ Mermaid diagram saved to: {output_path}")


if __name__ == "__main__":
    main()

import argparse
from pathlib import Path

from .fetcher import fetch_filters
from .generator import generate_unified_list


def main():
    parser = argparse.ArgumentParser(description="Generate Brave filter list")
    parser.add_argument('-o', '--output', type=Path, required=True, help='Output file path')
    args = parser.parse_args()

    data = fetch_filters()
    lines = generate_unified_list(data)

    with args.output.open('w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

if __name__ == '__main__':
    main()

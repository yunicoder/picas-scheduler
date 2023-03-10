from pathlib import Path

import yaml


def read_input(file_path: Path):
    with open(file_path, 'r') as yml:
        input = yaml.safe_load(yml)
    return input


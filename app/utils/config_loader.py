from typing import OrderedDict
import yaml
import yamlordereddictloader


def load_config(config_path: str) -> OrderedDict:
    with open(config_path, "r") as f:
        file = yaml.load(f, Loader=yamlordereddictloader.Loader)

    return file

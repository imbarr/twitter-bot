import sys
import yaml

_config = None


def get_config():
    global _config
    if _config is None:
        try:
            with open('config/config.yaml', 'r') as file:
                _config = yaml.load(file.read(), yaml.Loader)
        except Exception as err:
            print(f'Error reading config file: {repr(err)}', file=sys.stderr)
            sys.exit(1)
    return _config

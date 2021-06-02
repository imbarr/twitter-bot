import json
import sys
from types import SimpleNamespace

config = None

try:
    with open('config/config.json', 'r') as file:
        config = json.loads(file.read(), object_hook=lambda d: SimpleNamespace(**d))
except EnvironmentError as err:
    print(f'Error reading config file: {repr(err)}', file=sys.stderr)
    sys.exit(1)

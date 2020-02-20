import json
from typing import Dict

def load_env() -> Dict:
    with open('environment.json', 'r') as cp:
        env = json.load(cp)
    return env

import json
import os
from typing import Dict, List

def load_env() -> Dict:
    with open('environment.json', 'r') as cp:
        env = json.load(cp)
    return env


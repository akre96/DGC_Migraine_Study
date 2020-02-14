import json
from typing import Dict

def load_palette() -> Dict:
  with open('color_palette.json', 'r') as cp:
      palette = json.load(cp)
  return palette

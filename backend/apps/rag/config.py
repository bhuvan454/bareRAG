import sys
from pathlib import Path

core_path = Path(__file__).resolve().parents[2] / 'core'
# print(core_path)
sys.path.append(str(core_path))

from config import Config 


config = Config()

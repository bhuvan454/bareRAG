from qdrant_client import qdrant_client
from .config import config

# qudrant client setup

qdrant_client = QdarntClient(url = config.QDRANT_URL)


def get_qdrant_client():
    return qdrant_client
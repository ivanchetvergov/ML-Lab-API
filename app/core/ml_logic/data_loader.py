# app/core/ml_logic/data_loader.py
import numpy as np
from sklearn.datasets import make_classification

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def simulate_data_load(data_id: str):
    """
    симулирует загрузку датасета по data_id.
    в будущем сюда можно прикрутить загрузку реальных csv или sql.
    """
    # случайное зерно, чтобы data_id хоть что-то значил
    logger.info(f"[data_loader] loading synthetic dataset for id={data_id}")
    random_state = sum(ord(c) for c in data_id) % 1000
    X, y = make_classification(
        n_samples=200,
        n_features=5,
        n_informative=3,
        n_redundant=0,
        random_state=random_state
    )
    return X, y

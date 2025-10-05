# app/core/ml_logic/model_factory.py
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# словарь поддерживаемых моделей и допустимых параметров
MODEL_REGISTRY = {
    "LogisticRegression": {
        "class": LogisticRegression,
        "allowed_params": {"penalty", "C", "max_iter", "solver", "fit_intercept"}
    },
    "RandomForestClassifier": {
        "class": RandomForestClassifier,
        "allowed_params": {"n_estimators", "max_depth", "min_samples_split", "min_samples_leaf"}
    },
    "SVC": {
        "class": SVC,
        "allowed_params": {"C", "kernel", "degree", "gamma"}
    }
}

def init_model(model_type: str, params: dict):
    """
    инициализирует модель по названию и параметрам.
    фильтрует только разрешённые параметры.
    """
    if model_type not in MODEL_REGISTRY:
        raise ValueError(f"unsupported model type: {model_type}")

    model_info = MODEL_REGISTRY[model_type]
    allowed = model_info["allowed_params"]
    filtered = {k: v for k, v in params.items() if k in allowed}
    
    return model_info["class"](**filtered)

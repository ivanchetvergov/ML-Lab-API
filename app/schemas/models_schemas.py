from pydantic import BaseModel, Field, conint, confloat
from typing import Optional, Literal

# --- 1. Logistic Regression Params ---
class LogisticRegressionParams(BaseModel):
    penalty: Optional[Literal["l1", "l2", "elasticnet", "none"]] = Field(
        "l2", description="Norm of the penalty."
    )
    C: Optional[confloat(ge=0.01)] = Field( # type: ignore
        1.0, description="Inverse of regularization strength (>= 0.01)."
    ) 
    max_iter: Optional[conint(ge=1)] = Field( # type: ignore
        100, description="Max iterations for solvers."
    )
    solver: Optional[Literal["lbfgs", "liblinear", "newton-cg", "sag", "saga"]] = Field("lbfgs")

# --- 2. Random Forest Params ---
class RandomForestParams(BaseModel):
    n_estimators: Optional[conint(ge=1)] = Field( # type: ignore
        100, description="Number of trees in the forest."
    ) 
    max_depth: Optional[conint(ge=1)] = Field( # type: ignore
        None, description="Max depth of the tree (None = expansion until pure)."
    ) 
    min_samples_split: Optional[conint(ge=2)] = Field( # type: ignore
        2, description="Min samples required to split an internal node."
    ) 

# --- 3. Support Vector Classifier Params ---
class SVCParams(BaseModel):
    C: Optional[confloat(ge=0.01)] = Field( # type: ignore
        1.0, description="Regularization parameter (strictly positive)."
    ) 
    kernel: Optional[Literal["linear", "poly", "rbf", "sigmoid", "precomputed"]] = Field("rbf")
    gamma: Optional[Literal["scale", "auto"]] = Field("scale", description="Kernel coefficient.")
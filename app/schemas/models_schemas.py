from pydantic import BaseModel, Field, conint, confloat
from typing import Optional

class LogisticRegressionParams(BaseModel):
    penalty: Optional[str] = "l2"
    C: Optional[float] = 1.0
    max_iter: Optional[int] = 100

from pydantic import BaseModel


class FalcScore(BaseModel):
    good: str
    bad: str
    improve: str
    score: float

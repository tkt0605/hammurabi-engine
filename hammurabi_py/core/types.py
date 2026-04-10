from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field

class EvaluationContext(BaseModel):
    user_id: str
    action: str
    resource_id: str
    attributes: Dict[str, Any] = Field(default_factory=dict)

class TraceNode(BaseModel):
    rule_id: str
    condition: str
    passed: bool
    message: str

class EvaluationResult(BaseModel):
    allowed: bool
    reason: Optional[str] = None
    rule_id: Optional[str] = None
    trace: List[TraceNode] = Field(default_factory=list)
    confidence: float = 1.0
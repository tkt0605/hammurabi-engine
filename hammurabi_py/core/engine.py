from .types import EvaluationContext, EvaluationResult, TraceNode
from typing import List, Dict, Any
class HammurabiEngine:
    def __init__(self, policies: List[Dict[str, Any]]):
        self.policies = policies
    
    def evaluate(self, context: EvaluationContext, policy_name: str) -> EvaluationResult:
        policy = next(
            (p for p in self.policies if p["policy"] == policy_name),
            None
        )
        if not policy:
            return EvaluationResult(allowed=False, reason=f"Policy '{policy_name}' not found")
        trace = []
        for idx, rule in enumerate(policy["rules"]):
            condition = rule["condition"]
            is_match = self._check_condition(condition, context)
            trace.append(TraceNode(
                rule_id=f"{policy_name}_rule_{idx}",
                condition=condition,
                passed=is_match,
                message="Condition met" if is_match else "Condition not met"
            ))
            if not is_match:
                return EvaluationResult(
                    allowed=rule["allow"],
                    rule_id=f"{policy_name}_rule_{idx}",
                    trace=trace
                )
        return EvaluationResult(allowed=False, reason="No rules matched", trace=trace)
    def _check_condition(self, condition: str, context: EvaluationContext) -> bool:
        """
        AIが生成しやすい、あるいはパースしやすいシンプルな条件評価
        例: 'user.role == admin' -> context.attributes['role'] == 'admin'
        """
        try:
            scope = {
                "user": context.attributes.get("user", {}),
                "resource": context.attributes.get("resource", {}),
                "id": context.user_id
            }
            return eval(condition, {"__builtins__": {}}, scope)
        except Exception as e:
            return False
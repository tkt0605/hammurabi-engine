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
            condition = rule.get("if")
            if not condition:
                raise ValueError(f"Rule {idx} in policy '{policy_name}' must have an 'if' condition")
            is_match = self._check_condition(condition, context)
            trace.append(TraceNode(
                rule_id=f"{policy_name}_rule_{idx}",
                condition=condition,
                passed=is_match,
                message="Condition met" if is_match else "Condition not met"
            ))
            if is_match:
                return EvaluationResult(
                    allowed=rule["allow"],
                    rule_id=f"{policy_name}_rule_{idx}",
                    trace=trace
                )
            # 条件不一致の場合は次のルールへ継続
        return EvaluationResult(allowed=False, reason="No rules matched", trace=trace)
    def _check_condition(self, condition: str, context: EvaluationContext) -> bool:
        """
        AIが生成しやすい、あるいはパースしやすいシンプルな条件評価
        例: 'user.role == "admin"' -> context.attributes['user']['role'] == 'admin'
        dict をドット記法でアクセス可能にするため AttrDict でラップする。
        """
        class AttrDict(dict):
            def __getattr__(self, key: str):
                try:
                    val = self[key]
                    return AttrDict(val) if isinstance(val, dict) else val
                except KeyError:
                    raise AttributeError(key)

        try:
            scope = {
                "user": AttrDict(context.attributes.get("user", {})),
                "resource": AttrDict(context.attributes.get("resource", {})),
                "id": context.user_id
            }
            return bool(eval(condition, {"__builtins__": {}}, scope))
        except Exception:
            return False
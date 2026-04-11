import pytest
from hammurabi_py.core.engine import HammurabiEngine
from hammurabi_py.core.types import EvaluationContext

def test_admin_allow_rule():
    policies = [{
        "policy": "edit_policy",
        "rules": [
            {
                "if": "user.role == 'admin'",
                "allow": True
            },
        ]
    }]
    engine = HammurabiEngine(policies=policies)
    context = EvaluationContext(
        user_id = "1",
        action="edit",
        resource_id="post_123",
        attributes={
            "user": {
                "role": "admin"
            }
        }
    )
    ## policyのルールの名前を取得している。「edit_policy」を取得中
    result = engine.evaluate(context, "edit_policy")
    assert result.allowed is True
    assert result.rule_id == "edit_policy_rule_0"
    ## ここも問題
    assert any(t.passed for t in result.trace) is True
    
def test_invalid_rule():
    policies = [{"policy": "x", "rules": [{}]}]
    engine = HammurabiEngine(policies)
    with pytest.raises(Exception):
        engine.evaluate(EvaluationContext(
            user_id="1",
            action="edit",
            resource_id="post_123",
            attributes={}
        ), "x")

def test_non_admin_deny_rule():
    """非adminユーザーは allow されないことを確認"""
    policies = [{
        "policy": "edit_policy",
        "rules": [{"if": "user.role == 'admin'", "allow": True}]
    }]
    engine = HammurabiEngine(policies=policies)
    context = EvaluationContext(
        user_id="2",
        action="edit",
        resource_id="post_123",
        attributes={"user": {"role": "user"}}
    )
    result = engine.evaluate(context, "edit_policy")
    assert result.allowed is False

def test_policy_not_found():
    """存在しないポリシー名を指定した場合、allowed=False かつ reason に 'not found' を含む"""
    engine = HammurabiEngine(policies=[])
    context = EvaluationContext(
        user_id="1",
        action="edit",
        resource_id="post_123",
        attributes={}
    )
    result = engine.evaluate(context, "nonexistent_policy")
    assert result.allowed is False
    assert result.reason is not None and "not found" in result.reason

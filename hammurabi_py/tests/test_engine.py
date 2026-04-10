import os
import django
import pytest
from hammurabi_py.core.engine import HammurabiEngine
from hammurabi_py.core.types import EvaluationContext

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hammurabi_py.settings")
django.setup()

def test_admin_allow_rule():
    policies = [{
        "policy": "edit_policy",
        "rules": [
            {"if": "user.role == 'admin'", "allow": True},
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
    result = engine.evaluate(context, "edit_policy")
    assert result.allowed is True
    assert result.rule_id == "edit_policy_rule_0"
    assert any(t.passed for t in result.trace) is True

def test_engine_evaluation():
    policies = [
        {
            "policy": "test_policy",
            "rules": [
                {"condition": "user['role'] == 'admin'", "allow": True},
                {"condition": "user['role'] == 'user'", "allow": False}
            ]
        }
    ]
    engine = HammurabiEngine(policies=policies)
    
    context_admin = EvaluationContext(
        user_id="1",
        action="read",
        resource_id="res1",
        attributes={"user": {"role": "admin"}}
    )
    result_admin = engine.evaluate(context_admin, "test_policy")
    assert result_admin.allowed == True
    assert len(result_admin.trace) == 1
    assert result_admin.trace[0].passed == True
    
    context_user = EvaluationContext(
        user_id="2",
        action="read",
        resource_id="res1",
        attributes={"user": {"role": "user"}}
    )
    result_user = engine.evaluate(context_user, "test_policy")
    assert result_user.allowed == False
    assert len(result_user.trace) == 1
    assert result_user.trace[0].passed == False

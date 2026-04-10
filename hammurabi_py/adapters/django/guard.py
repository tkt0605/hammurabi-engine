from functools import wraps
from django.http import JsonResponse
from hammurabi_py.core.engine import HammurabiEngine, EvaluationContext

_engine = HammurabiEngine(policies=[])

def guard(policy_name: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            context = EvaluationContext(
                user_id = str(request.user.id) if request.user.is_authenticated else "anonymous",
                action = request.method,
                resource_id=str(kwargs.get('pk', 'global')),
                attributes={
                    "user": {
                        "role": "admin" if request.user.is_superuser else "user"
                    },
                    "resource": {
                        "author_id": "1"
                    }
                }
            )
            result = _engine.evaluate(context, policy_name)
            if result.allowed:
                request.auth_trace = result.trace
                return view_func(request, *args, **kwargs)
            
            return JsonResponse({
                "error": "Forbidden",
                "reason": result.reason,
                "trace": [t.dict() for t in result.trace]
            }, status=403)
        return _wrapped_view
    return decorator
import os
import django
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from hammurabi_py.adapters.django.guard import guard
from django.http import JsonResponse, HttpRequest, HttpResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hammurabi_py.settings")
django.setup()
def test_guard_decorator_denies_anonymous(rf):
    @guard("test_policy")
    def mock_view(request):
        return HttpResponse("Success")
    request = rf.get("/edit/1")
    request.user = User(is_authenticated=False)

    response = mock_view(request)
    assert response.status_code == 403
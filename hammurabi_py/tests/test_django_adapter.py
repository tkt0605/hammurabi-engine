from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest, HttpResponse
from hammurabi_py.adapters.django.guard import guard
def test_guard_decorator_denies_anonymous(rf):
    @guard("test_policy")
    def mock_view(request):
        return HttpResponse("Success")
    request = rf.get("/edit/1")
    request.user = AnonymousUser()

    response = mock_view(request)
    assert response.status_code == 403
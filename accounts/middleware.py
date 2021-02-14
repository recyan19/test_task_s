from django.utils import timezone
from django.http.response import HttpResponse
from accounts.models import Profile

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user


def get_user_jwt(request):
    user = get_user(request)
    if user.is_authenticated:
        return user
    try:
        user_jwt = JWTAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            return user_jwt[0]
    except:
        pass
    return user


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.user = SimpleLazyObject(lambda: get_user_jwt(request))
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user__id=request.user.id).first()
            if profile:
                profile.last_activity = timezone.now()
                profile.save()
            else:
                Profile.objects.create(user=request.user, last_activity=timezone.now())

import django
# Django 1.5 add support for custom auth user model
if django.VERSION >= (1, 5):
    from django.contrib.auth import get_user_model
    User = get_user_model()
else:
    try:
        from django.contrib.auth.models import User
    except ImportError:
        raise ImportError(u'User model is not to be found.')
from django.conf import settings
from django.contrib.auth import login

from tempus.middleware import BaseTempusMiddleware


class AutoLoginMiddleware(BaseTempusMiddleware):
    def _get_user(self, request):
        user_pk = request.tempus
        if user_pk:
            # Only change user if necessary. We strip the token in any case.
            # The AnonymousUser class has no 'pk' attribute (#18093)
            if getattr(request.user, 'pk', request.user.id) == user_pk:
                return None
            try:
                return User.objects.get(pk=user_pk)
            except (ValueError, User.DoesNotExist):
                return None

    def success_func(self, request):
        user = self._get_user(request)
        if user:
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)

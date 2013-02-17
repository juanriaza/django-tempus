from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers
from django.core.signing import BadSignature, SignatureExpired

from urlobject import URLObject

from .utils import tempus_loads


class BaseTempusMiddleware(object):
    max_age = None
    param_name = 'tempus'

    def process_request(self, request):
        token = request.GET.get(self.param_name)
        if not token:
            return

        redirect_url = URLObject(request.get_full_path())
        redirect_url = redirect_url.del_query_param(self.param_name)

        response = redirect(unicode(redirect_url))
        try:
            token_data = tempus_loads(token, max_age=self.max_age)
        except SignatureExpired:
            expired_func = getattr(self, 'expired_func')
            if expired_func:
                expired_func(request, token_data)
        except BadSignature:
            return response
        else:
            self.success_func(request, token_data)

            add_never_cache_headers(response)
            return response

    def success_func(self, request, token_data):
        raise NotImplementedError

    def expired_func(self, request, token_data):
        raise NotImplementedError

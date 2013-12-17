from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers
from django.core.signing import BadSignature
from django.core.signing import SignatureExpired

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
            tempus = getattr(request, 'tempus', None)
            if tempus:
                current_tempus = tempus.copy()
                request.tempus = current_tempus.update(token_data)
            else:
                request.tempus = token_data
        except SignatureExpired:
            expired_func = getattr(self, 'expired_func', None)
            if expired_func:
                value = expired_func(request)
                if isinstance(value, HttpResponseRedirect):
                    return value
        except BadSignature:
            return response
        else:
            success_func = getattr(self, 'success_func', None)
            if success_func:
                value = success_func(request)
                if isinstance(value, HttpResponseRedirect):
                    return value

            add_never_cache_headers(response)
            return response

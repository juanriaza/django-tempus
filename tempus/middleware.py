from django.http import HttpResponse
from django.shortcuts import redirect
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
                current_tempus.update(token_data)
                request.tempus = current_tempus
            else:
                request.tempus = token_data
        except SignatureExpired:
            value = self.__process_func(request, 'expired_func')
            if value:
                return value
        except BadSignature:
            value = self.__process_func(request, 'unsuccess_func')
            if value:
                return value
        else:
            value = self.__process_func(request, 'success_func')
            if value:
                return value

        add_never_cache_headers(response)
        return response

    def __process_func(self, request, func_name):
        func_name = getattr(self, func_name, None)
        if func_name:
            value = func_name(request)
            if isinstance(value, HttpResponse):
                return value

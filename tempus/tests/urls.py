from __future__ import unicode_literals

from django.conf.urls import patterns

from .utils import show_user, promo


urlpatterns = patterns('', (r'^user/$', show_user), (r'^promo/$', promo))

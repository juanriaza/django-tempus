from __future__ import unicode_literals

from django.conf.urls import patterns

from .views import promo
from .views import show_user


urlpatterns = patterns('', (r'^user/$', show_user), (r'^promo/$', promo))

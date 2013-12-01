from django.http import HttpResponse
from django.template import RequestContext
from django.template import Template


template_user = Template(
    '{% if user.is_authenticated %}{{ user }}'
    '{% elif user.is_anonymous %}anonymous'
    '{% else %}no user'
    '{% endif %}'
)

template_promo = Template(
    '{{ price }}'
)


def show_user(request):
    context = RequestContext(request)
    return HttpResponse(template_user.render(context),
                        content_type='text/plain')


def promo(request):
    price = 25
    discount = request.tempus.get('discount', 0)
    price -= discount
    context = RequestContext(request, {'price': price})
    return HttpResponse(template_promo.render(context),
                        content_type='text/plain')

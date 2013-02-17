# Django Tempus

[![Build Status](https://travis-ci.org/juanriaza/django-tempus.png?branch=master)](https://travis-ci.org/juanriaza/django-tempus)



## Overview

Django Tempus provides url tokens that triggers custom actions.

## Installation

Install using `pip`, including any optional packages you want...
	
	$ pip install django-tempus

...or clone the project from github.

    $ git clone git@juanriaza/django-tempus.git
    $ cd django-tempus
    $ pip install -r requirements.txt

## How to use it?

We own the `Awesome Shop` where you can find the finest rockets…

![image](https://www.django-shop.org/media/img/theme/django-pony-shop.png)

Rockets are pricey… and every single cool pony out there wants one.

We want to boost our sales and we offer a discount and mail it to those cute ponies.

Let's go!

```python
from tempus.middleware import BaseTempusMiddleware


class RocketDiscountMiddleware(BaseTempusMiddleware):
    param_name = 'rocket_promo'

    def success_func(self, request, token_data):
        discount = token_data.get('discount')
        if discount:
            request.session['discount'] = discount
```

We need to add the `RocketDiscountMiddleware` to `MIDDLEWARE_CLASSES` at `settings.py`

```python
MIDDLEWARE_CLASSES = (
	...
    'awesomeshop.products.middleware.RocketDiscountMiddleware'
)
```

And get the discount:

```python
def rocket_view(request, rocket_model):
	rocket_price = Rocket.objects.get(model=rocket_model).price
	discount = request.session.get('discount', 0)
	rocket_price -= discount
	return render('awesome/template.html', {'price': rocket_price})
```


We're done.

Now we can send special tokenized urls with the discount to our beloved ponies

```
{% load tempus %}

Hi {{ pony_name }},

Just because you rock we offer you a discount on our ultimate X-ROCKET 3K.

{% url 'rocket_url' %}{% tempus {'discount': 500} param_key='rocket_promo' %}
```


## Running the tests
To run the tests against the current environment:

    $ django-admin.py test tempus --settings=tempus.tests.settings

## Changelog

### 0.1.0

**17th Feb 2012**

* First release.

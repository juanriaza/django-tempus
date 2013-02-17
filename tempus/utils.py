from django.core import signing


def tempus_dumps(data, salt='tempus'):
    encrypted_data = signing.dumps(data, salt=salt)
    return encrypted_data


def tempus_loads(encrypted_data, salt='tempus', max_age=None):
    data = signing.loads(encrypted_data, salt=salt, max_age=max_age)
    return data

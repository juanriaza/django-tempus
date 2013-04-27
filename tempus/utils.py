from django.core import signing


def tempus_dumps(data, salt='tempus', compress=True, *args, **kwargs):
    encrypted_data = signing.dumps(
        data, salt=salt, compress=compress, *args, **kwargs)
    return encrypted_data


def tempus_loads(encrypted_data, salt='tempus', max_age=None, *args, **kwargs):
    data = signing.loads(
        encrypted_data, salt=salt, max_age=max_age, *args, **kwargs)
    return data

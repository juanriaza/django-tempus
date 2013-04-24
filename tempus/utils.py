from django.core import signing


def tempus_dumps(data, salt='tempus', compress=True, *args, **kwargs):
    encrypted_data = signing.dumps(data, salt=salt, compress=compress, *args, **kwargs)
    if compress:
        return encrypted_data[1:]
    return encrypted_data


def tempus_loads(encrypted_data, salt='tempus', max_age=None, compress=True, *args, **kwargs):
    if compress:
        encrypted_data = '.%s' % encrypted_data
    data = signing.loads(encrypted_data, salt=salt, max_age=max_age, *args, **kwargs)
    return data

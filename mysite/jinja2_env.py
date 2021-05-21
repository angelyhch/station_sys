from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
from craft.utils import set_craft_global


def filter_trim_quote(string):
    temp = string.replace('\'', '')
    result = temp.replace('\"', '')
    return result


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.globals.update(set_craft_global())

    env.filters['filter_trim_quote'] = filter_trim_quote

    return env

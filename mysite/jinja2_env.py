from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
from craft.utils import set_craft_global

from sorl.thumbnail import get_thumbnail

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.globals.update(set_craft_global())
    return env

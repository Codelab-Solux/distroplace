from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from hashids import Hashids
from django.conf import settings
from django.core.paginator import Paginator
from datetime import date, timedelta


def get_tomorrow():
    return date.today() + timedelta(days=1)

# custom ID hasher ------------------------------
hashids = Hashids(settings.HASHIDS_SALT, min_length=8)


def h_encode(id):
    return hashids.encode(id)


def h_decode(h):
    z = hashids.decode(h)
    if z:
        return z[0]


class HashIdConverter:
    regex = '[a-zA-Z0-9]{8,}'

    def to_python(self, value):
        return h_decode(value)

    def to_url(self, value):
        return h_encode(value)

# custom paginator ------------------------------
def paginate_objects(req, obj_list, obj_count=12):
    p = Paginator(obj_list, obj_count)
    page = req.GET.get('page')
    objects = p.get_page(page)
    return objects



# token generator ------------------------------
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type((user.id))+six.text_type((timestamp))+six.text_type(user.email_verified))

generate_token = TokenGenerator()


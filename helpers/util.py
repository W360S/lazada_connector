import operator
import re
from odoo.http import request

import logging

from odoo.models import Model

_logger = logging.getLogger(__name__)


def check_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def hidden_phone(str):
    phones = re.findall('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', str,
                        re.MULTILINE)
    for phone in phones:
        p = re.search('(.*)(...)$', phone).groups()
        h = re.sub('\d', '*', p[0])
        str = re.sub(phone, "%s%s" % (h, p[1]), str)
    return str


def get_image_url(instance: Model, field: str, size_default=512):
    instance.ensure_one()
    if not isinstance(operator.attrgetter(field)(instance), bytes):
        return f'https://via.placeholder.com/{size_default}'
    return f'{request.httprequest.url_root}web/image?model={instance._name}&field={field}&id={instance.id}'


def get_text_selection(data: Model, field: str):
    try:
        return dict(data.fields_get().get(field).get('selection', False)).get(getattr(data, field))
    except Exception:
        return 'Not found'

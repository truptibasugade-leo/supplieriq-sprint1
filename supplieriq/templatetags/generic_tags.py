from django import template
register = template.Library()
from django.core.serializers import serialize
from django.db.models.query import QuerySet
# from django.utils import simplejson
import json

def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)

register.filter('jsonify', jsonify)

@register.simple_tag
def get_json(data):
    return json.dumps(dict(data))

@register.simple_tag
def format_label(data):
    return data.title()

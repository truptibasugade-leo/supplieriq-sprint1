from django import template
register = template.Library()
from django.core.serializers import serialize
from django.db.models.query import QuerySet
# from django.utils import simplejson
import json
import datetime

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
    vv= data.title()
    if vv.find("_") != -1:
        label = vv.replace("_"," ")
    else:
        label = vv
    return label
@register.simple_tag
def convert_to_date(data):
    v = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%SZ')
    return v.date()

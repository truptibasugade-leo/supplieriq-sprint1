from django import template
register = template.Library()
import json


@register.simple_tag
def get_json(data):
    return json.dumps(dict(data))

@register.simple_tag
def format_label(data):
    return data.title()

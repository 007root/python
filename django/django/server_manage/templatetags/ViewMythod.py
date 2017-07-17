from django import template
register = template.Library()

@register.simple_tag
def transform_list(data):
    data = str(data)
    data = data.split(',')
    data = map(lambda x:float(x),data)
    return data
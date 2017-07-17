from django import template
register = template.Library()

@register.simple_tag
def ipfilter(IP):
    IP = IP.split(':')[0]
    return IP




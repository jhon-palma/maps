from django import template
register = template.Library()

@register.filter
def pluck(queryset, key):
    return [d.get(key) for d in queryset]

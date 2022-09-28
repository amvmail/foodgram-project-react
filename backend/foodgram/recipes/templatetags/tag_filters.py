from django import template

register = template.Library()


@register.filter
def get_filter_tags(request, tag):
    new_request = request.GET.copy()
    tags = set(request.GET.getlist('tags'))
    if tag in tags:
        tags.remove(tag)
    else:
        tags.add(tag)
    new_request.setlist('tags', list(tags))
    return new_request.urlencode()

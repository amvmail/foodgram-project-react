from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


def required_edit(user, author) -> bool:
    return user == author

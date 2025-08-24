from django import template

register = template.Library()


@register.filter(name='add_classes')
def add_classes(value, arg):
    """
    Add CSS classes to form field
    Usage: {{ form.field|add_classes:"class1 class2" }}
    """
    return value.as_widget(attrs={'class': arg})

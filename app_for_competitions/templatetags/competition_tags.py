from django import template

register = template.Library()


@register.filter
def my_getattr(row, field_name, default=None):
    return getattr(row, field_name, default)

# @register.filter
# def getattr (obj, args):
#     """ Try to get an attribute from an object.
#     Example: {% if block|getattr:"editable,True" %}
#     Beware that the default is always a string, if you want this
#     to return False, pass an empty second argument:
#     {% if block|getattr:"editable," %}
#     """
#     (attribute, default) = args.split(',')
#     try:
#         return obj.__getattribute__(attribute)
#     except AttributeError:
#          return  obj.__dict__.get(attribute, default)
#     except:
#         return default

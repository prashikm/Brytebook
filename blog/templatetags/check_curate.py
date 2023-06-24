from django import template
register = template.Library()
from blog.models import Post

@register.filter(name='check_curate')
def check_curate(curate_object, user):
    the_curate = curate_object.curate.filter(username=user)
    is_curated = True if the_curate else False
    return is_curated

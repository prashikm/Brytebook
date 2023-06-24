from django import template
register = template.Library()


@register.filter(name='check_bookmark')
def check_bookmark(bookmark_object, user):
    the_bookmark = bookmark_object.bookmark.filter(username=user)
    is_bookmarked = True if the_bookmark else False
    return is_bookmarked

from django.templatetags.static import *
from django.urls import reverse
from django.conf import settings

register = Library()

class StaticNode(OriginalStaticNode):

    def url(self, context):
        path = super().url(context)
        if not settings.DEBUG:
            path = reverse('static', kwargs={'path': path})
        return path

@register.tag('static')
def do_static(parser, token):
    return StaticNode.handle_token(parser, token)

from django.template import Library, Node, TemplateSyntaxError, Variable
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

class InboxOutput(Node):
    def __init__(self, varname=None):
        self.varname = varname
        
    def render(self, context):
        try:
            user = context['user']
            count = user.received_messages.filter(read_at__isnull=True, recipient_deleted_at__isnull=True).count()
        except (KeyError, AttributeError):
            count = ''
        if self.varname is not None:
            context[self.varname] = count
            return ""
        else:
            return "%s" % (count)        
        
def do_print_inbox_count(parser, token):
    """
    A templatetag to show the unread-count for a logged in user.
    Returns the number of unread messages in the user's inbox.
    Usage::
    
        {% load inbox %}
        {% inbox_count %}
    
        {# or assign the value to a variable: #}
        
        {% inbox_count as my_var %}
        {{ my_var }}
        
    """
    bits = token.contents.split()
    if len(bits) > 1:
        if len(bits) != 3:
            raise TemplateSyntaxError, "inbox_count tag takes either no arguments or exactly two arguments"
        if bits[1] != 'as':
            raise TemplateSyntaxError, "first argument to inbox_count tag must be 'as'"
        return InboxOutput(bits[2])
    else:
        return InboxOutput()

register = Library()     
register.tag('inbox_count', do_print_inbox_count)

@register.tag
def report_spam_url(parser, token): 
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("Accepted format {% vendor_follower_info_url [instance] %}")
    else:
        return ReportSpam(*bits[1:])

class ReportSpam(Node):
    def __init__(self, obj):
        self.obj = Variable(obj)

    def render(self, context):
        obj_instance = self.obj.resolve(context)
        content_type = ContentType.objects.get_for_model(obj_instance).pk
        return reverse('report_spam', kwargs={'content_type_id': content_type, 'object_id': obj_instance.pk })

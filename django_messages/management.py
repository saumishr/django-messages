from django.db.models import get_models, signals
from django.conf import settings
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notifications(app, created_models, verbosity, **kwargs):
        notification.NoticeType.create("messages_received", _("Message Received"), _("you have received a message"), default=2)
        notification.NoticeType.create("messages_sent", _("Message Sent"), _("you have sent a message"), default=1)
        notification.NoticeType.create("messages_replied", _("Message Replied"), _("you have replied to a message"), default=1)
        notification.NoticeType.create("messages_reply_received", _("Reply Received"), _("you have received a reply to a message"), default=2)
        notification.NoticeType.create("messages_deleted", _("Message Deleted"), _("you have deleted a message"), default=1)
        notification.NoticeType.create("messages_recovered", _("Message Recovered"), _("you have undeleted a message"), default=1)

    signals.post_syncdb.connect(create_notifications, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"

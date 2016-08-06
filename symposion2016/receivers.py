from django.dispatch import receiver
from django.db.models.signals import post_save

from account.signals import password_changed
from account.signals import user_sign_up_attempt, user_signed_up
from account.signals import user_login_attempt, user_logged_in

from eventlog.models import log
from pycon_proposals.models import TalkProposal, TutorialProposal
from .notifiers import WebhookNotifier


@receiver(user_logged_in)
def handle_user_logged_in(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_LOGGED_IN",
        extra={}
    )


@receiver(password_changed)
def handle_password_changed(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="PASSWORD_CHANGED",
        extra={}
    )


@receiver(user_login_attempt)
def handle_user_login_attempt(sender, **kwargs):
    log(
        user=None,
        action="LOGIN_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_sign_up_attempt)
def handle_user_sign_up_attempt(sender, **kwargs):
    log(
        user=None,
        action="SIGNUP_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "email": kwargs.get("email"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_SIGNED_UP",
        extra={}
    )


@receiver(post_save, sender=TalkProposal)
def talk_created(sender, instance, created, **kwargs):
    if created:
        message = "{speaker} has submitted a {kind} proposal: \"{title}\"".format(
            speaker=instance.speaker.name,
            kind='talk',
            title=instance.title
        )
        WebhookNotifier.notify(data=message, params={'channel': '#programme'})


@receiver(post_save, sender=TutorialProposal)
def tutorial_created(sender, instance, created, **kwargs):
    if created:
        message = "{speaker} has submitted a {kind} proposal: \"{title}\"".format(
            speaker=instance.speaker.name,
            kind='tutorial',
            title=instance.title
        )
        WebhookNotifier.notify(data=message, params={'channel': '#programme'})

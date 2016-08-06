import requests
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.conf import settings


class WebhookNotifier(object):
    webhook_conf = getattr(settings, 'WEBHOOKS', {})
    url_validator = URLValidator()

    @classmethod
    def url_valid(cls, url):
        try:
            cls.url_validator(url)
        except ValidationError:
            return False

        return True

    @classmethod
    def notify(cls, webhook=None, **request_kwargs):
        webhook = cls.webhook_conf.get(webhook or 'default')
        if webhook:
            for k in webhook:
                if isinstance(webhook[k], dict) and k in request_kwargs:
                    webhook[k].update(request_kwargs.pop(k))
                elif k in request_kwargs:
                    webhook[k] = request_kwargs.pop(k)
            webhook.update(request_kwargs)

            if cls.url_valid(webhook.get('url')):
                requests.post(**webhook)

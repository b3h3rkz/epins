# -*- coding: utf-8 -*-
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from wallet.models import Wallet

class AccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        context['activate_url'] = settings.URL_FRONT + \
            'access/verify-email/' + context['key']
        msg = self.render_mail(template_prefix, email, context)
        msg.content_subtype = 'html' 
        msg.send()


    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from barbary.users.views import (
    null_view,
    confirm_email,
    UserModelViewSet,
    UserAnalyticsModelViewSet,
    UserLoginHistoryModelViewSet
)
from currency.views import CurrencyModelViewSet, CurrencyPublicListModelViewSet
from orders.views import (
    BuyOrdersModelViewSet,
    AdminBuyOrdersModelViewset,
)
from wallet.views import (WalletModelViewSet,
                          AdminWalletModelViewSet, 
                          DepositModelViewSet,
                          ManualDepositModelViewSet, )

from bills.views import ServiceModelViewSet
from country.views import CountryModelViewSet
from rest_framework import routers

router = routers.DefaultRouter()


router.register(r'logins', UserLoginHistoryModelViewSet, base_name='logins')
router.register(r'buy_orders', BuyOrdersModelViewSet, base_name='buy_orders')
router.register(r'users', UserModelViewSet, base_name='user_acct')
router.register(r'deposits', DepositModelViewSet, base_name='deposits')
router.register(r'manual_deposit', ManualDepositModelViewSet, base_name='manual_deposits')
router.register(r'countries', CountryModelViewSet, base_name='countries')
router.register(r'wallets', WalletModelViewSet, base_name='admin_wallets')
router.register(r'currencies', CurrencyModelViewSet)


urlpatterns = [
     # Django Admin, use {% url 'admin:index' %}
     url(settings.ADMIN_URL, admin.site.urls),
    #  url(r'^', include('django.contrib.auth.urls')),
     url(r'^', include('rest_framework_docs.urls')),

    #  url(r'^$', schema_view),

     url(r'^accounts/', include('allauth.urls')),
     #auth urls
     url(r'^rest-auth/registration/account-email-verification-sent/', null_view, name='account_email_verification_sent'),
     url(r'^rest-auth/registration/account-confirm-email/', null_view, name='account_confirm_email'),
     url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',null_view, name='password_reset_confirm'),
     url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
     url(r'^verify-email/(?P<key>\w+)/$', confirm_email, name="account_confirm_email"),
     url(r'^api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
     url(r'^auth/v1/api-token-auth/', obtain_jwt_token),
     url(r'^api-token-refresh/', refresh_jwt_token),
     url(r'^docs/', include('rest_framework_docs.urls')),
     url(r'^api/v1/', include(router.urls), name='home'),
     url(r'^api/v1/test', include('orders.urls')),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
                 url(r'^debug/', include(debug_toolbar.urls)), ]






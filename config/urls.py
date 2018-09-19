# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
# from rest_framework.documentation import include_docs_urls

from barbary.users.views import (
    null_view,
    confirm_email,
    UserModelViewSet,
    UserAnalyticsModelViewSet,
    AdminUserModelViewSet,
    UserLoginHistoryModelViewSet
)

from shapeshift.views import ShiftListModelView
from currency.views import CurrencyModelViewSet, CurrencyPublicListModelViewSet
from orders.views import (
    BuyOrdersModelViewSet,
    AdminBuyOrdersModelViewset,
    SellOrderModelViewset,
    AdminSellOrdersModelViewSet,
    AdminOrderAnalyticsModelViewSet,
)
from wallet.views import (WalletModelViewSet,
                          AdminWalletModelViewSet, 
                          DepositModelViewSet,
                          ManualDepositModelViewSet,
                          BeneficiaryBankModelViewSet,
                          BeneficiaryMobileMoneyModelViewSet,
                          WithdrawalModelViewSet, )

from bills.views import ServiceModelViewSet
from country.views import CountryModelViewSet
from shapeshift.views import ShiftModelViewSet
from rest_framework import routers
# from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
# schema_view = get_swagger_view(title='Bitnob API')


router.register(r'logins', UserLoginHistoryModelViewSet, base_name='logins')
router.register(r'buy_orders', BuyOrdersModelViewSet, base_name='buy_orders')
router.register(r'sell_orders', SellOrderModelViewset, base_name='sell_order')
router.register(r'shifts', ShiftModelViewSet, base_name='shifts')
router.register(r'users', UserModelViewSet, base_name='user_acct')
router.register(r'beneficiary_bank_accounts', BeneficiaryBankModelViewSet,
                base_name='beneficiary_bank_accounts')
router.register(r'beneficiary_momo_accounts', BeneficiaryMobileMoneyModelViewSet,
                base_name='beneficiary_momo_accounts')
router.register(r'deposits', DepositModelViewSet, base_name='deposits')
router.register(r'manual_deposit', ManualDepositModelViewSet, base_name='manual_deposits')
router.register(r'withdrawals', WithdrawalModelViewSet, base_name='withdrawals')
router.register(r'countries', CountryModelViewSet, base_name='countries')
router.register(r'wallets', WalletModelViewSet, base_name='admin_wallets')
router.register(r'user_analytics', UserAnalyticsModelViewSet)
router.register(r'currencies', CurrencyModelViewSet)
router.register(r'public-currencies', CurrencyPublicListModelViewSet)
router.register(r'services', ServiceModelViewSet)
router.register(r'analytics', AdminOrderAnalyticsModelViewSet, base_name='admin_analytics')


router.register(r'admin_users', AdminUserModelViewSet, base_name='admin_users')
router.register(r'admin_buy_orders', AdminBuyOrdersModelViewset, base_name='admin_buy_orders')
router.register(r'admin_sell_orders', AdminSellOrdersModelViewSet, base_name='admin_sell_orders')

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
    #  url(r'^api/shifts/', include('shapeshift.urls'), name='shapeshift')

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
                 url(r'^debug/', include(debug_toolbar.urls)), ]






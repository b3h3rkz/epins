from django.conf.urls import url
from .views import (
    CurrencyPublicListModelView,
)

# #
# urlpatterns = [
#      url(r'^$', CurrencyPublicListModelView.as_view(), name='list'),
# #     url(r'^add_currency/', CreateCurrencyModelView.as_view(), name='add'),
# #     url(r'^(?P<pk>[0-9]+)/$', CurrencyDetailModelView.as_view(), name='currency-detail'),
# #     url(r'^edit/(?P<pk>[0-9]+)/$', CurrencyUpdateModelView.as_view(), name='edit'),
# #     url(r'^delete/(?P<pk>[0-9]+)/$', DeleteCurrencyModelView.as_view(), name='delete'),
# #
# ]

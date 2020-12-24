import string
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.decorators import (
    list_route,
    detail_route
)
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response

from .serializers import VoucherModelSerializer
from .models import Voucher
from business.models import BusinessUnit
from barbary.users.models import User


class VoucherModelViewset(ModelViewSet):
    model = Voucher
    serializer_class = VoucherModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = Voucher.objects.all()

    def create(self, request, *args, **kwargs):
        # get business unit id
        business_unit = BusinessUnit.objects.get(id=request.data['business_unit'])
        voucher_length = business_unit.voucher_length

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # generate a voucher according to voucher_length and save
        serializer.save(
            pin=''.join(random.choice(string.digits) for _ in range(voucher_length))
        )
        return Response(
            data=serializer.data,
            status=HTTP_201_CREATED,
            headers=self.get_success_headers(serializer)
        )
    
    @list_route(methods=['POST',])
    def send_vouchers_by_email(self, request):
        user = User.objects.filter(pk=request.user.id)
        voucher = Voucher.objects.get(id=request.data['voucher_id'])
        voucher_pin = voucher.pin
        voucher_business_unit = voucher.business_unit.name
        
        # send email setup
        email = voucher.business_unit.merchant.email
        username = voucher.business_unit.merchant.username
        subject = "Voucher Pin"
        button_text = "View Accounts"

        # email template variables
        ctx = {
            'subject': subject,
            'main_button_text': button_text,
            'activity_name': subject,
            'business_unit_name': voucher_business_unit,
            'voucher_pin': voucher_pin,
            'user': username,
            'user_email': email,
        }

        message = render_to_string('account/email/voucher_email.html', context=ctx)

        msg = EmailMessage()
        msg.subject = subject
        msg.body = message
        msg.to = [email,]
        msg.content_subtype = 'html'
        msg.send()

        return Response(
            data={"message": "Working", "status": 200}
        )
from __future__ import absolute_import, unicode_literals
from allauth.account.views import ConfirmEmailView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .models import User, UserLoginHistory
from .serializers import (
    UserModelSerializer, 
    VerifyEmailSerializer,
    UserAnalytics, 
    AdminUserModelSerializer,
    UserLoginHistorySerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    list_route, 
    detail_route
)
from rest_framework.response import Response
import cloudinary
import cloudinary.uploader
import cloudinary.api
import nexmo
from .kyc_verification import *
from utils.utilfuncs import *
from random import randint


# def send_sms(phone_number, sms_code):
#     url = 'http://cheapglobalsms.com/api_v1'
#     params = {
#         'sub_account': '2132_bitcoin',
#         'sub_account_pass': 'diamond',
#         'action': 'send_sms',
#         'route': 0,
#         'sender_id': 'Diamond',
#         'recipients': +2348068476165,
#         'message': sms_code
#     }
#     send_sms = requests.post(url, params=params)
#     print(send_sms.text)
#     return send_sms.text


def hubtel_sms(phone_number, code):
    url = "https://api.hubtel.com/v1/messages/send"
    params = {
        "From": "Bitnob",
        "To": str(phone_number),
        "Content": str(code),
        "ClientId": "eaqhfpto",
        "ClientSecret": "medxbcgv",
        "RegisteredDelivery": "true"
    }
    response = requests.get(url, params=params, auth=('eaqhfpto', 'medxbcgv'))
    print(response.text)


def send_sms(q, b):
    url = 'http://cheapglobalsms.com/api_v1'
    params = {
            'sub_account': '2132_bitcoin',
            'sub_account_pass': 'diamond',
            'action': 'send_sms',
            'sender_id': 'Bitnob',
            'route': 2,
            # 'recipients': +233548075933,
            'type':0,
            'recipients': "+233545247030",
            'message': str(b)
    }
    # print(params)
    send_sms = requests.post(url, params=params)
    print(send_sms.text, b)
    return send_sms.text

@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView, ConfirmEmailView):
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)


confirm_email = VerifyEmailView.as_view()


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


class UserModelViewSet(ModelViewSet):
    """
    User Endpoints 
    """
    model = User
    permission_classes = [IsAuthenticated]
    # queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @list_route(methods=['[POST', 'PUT'])
    def uploads(self, request):
        """
        Endpoint for all uploads, the response message from cloudinary will be used to process the url 
        """
        image = cloudinary.uploader.upload(request.data['file'], folder='bitnob')
        return Response(image)

    @detail_route(methods=['[POST', 'GET','PUT'])
    def send_verification_sms(self, request, pk=None):
        """
        Send Verification SMS to the user's phone
        """
        user = User.objects.get(pk=pk)
        # user.phone = '+' + user.country.phone_code
        if user.country.name == 'Ghana':
            user.country.phone_code = '+234'
        if user.country.name == "Nigeria":
            user.country.phone_code = "+234"
        user.phone = '+' + user.country.phone_code
        user.phone += str(request.data['phone'])
        sms_code = randint(1000, 9999)
        hubtel_sms()
        sms_client = send_sms(user.phone, sms_code)
        if 'batch_id' in sms_client:
            user.id_number = sms_code
            user.save()
            return Response(data={
                    "message": "Code sent successfully",
                    "status": 200})
        else:
            return Response(data={
                    "message": "oops, something has happened, try again please"}, status=400)

    @detail_route(methods=['[POST', 'GET', 'PUT'])
    def verify_sms_code(self, request, pk=None):
        """
         Verify SMS code that was sent
        """
        user = User.objects.get(pk=pk)
        if request.data['code'] == user.id_number:
            user.verified_phone = True
            user.save()
            return Response(data={
                    "message": "Confirmed Phone Number Successfully",
                    "status": 200})
        else:
            return Response(data={
                    "message": "oops, something has happened, try again please"}, status=400)

    @detail_route(methods=['PUT'])
    def verify_account(self, request, pk=None):
        """
        Send a request to check the Account  Number submitted. This only works for Nigerian accounts
        :param request:
        :return: Response
        """
        user = User.objects.get(pk=pk)
        fullname = user.first_name + " " + user.last_name
        verified = verify_bank_acct(request.data['account_number'], request.data['bank_code'], fullname)
        if verified:
            user.verification_completed = True
            user.save()
            return Response(data={
                    "message": "Confirmed Account Successfully",
                    "status": 200})
        else:
            return Response(data={
                    "message": "oops, something has happened, try again please"}, status=400)

    @detail_route(methods=['PUT'])
    def verify_inclusive(self, request, pk=None):
        """
        verify Ghanaian accounts using this endpoint
        :param request:
        :return: `Response Json`
        """
        instance = self.get_object()
        verification_name = []
        id_number = request.data['id_number']
        fullname = " {} {}".format(request.user.first_name, request.user.last_name)
        fullname = transform_name(fullname)
        if request.data['method'] == 'Passport':
            verification_name = inclusive_passport(id_number)
        if request.data['method'] == 'SSNIT':
            verification_name = inclusive_ssnit(id_number)
        if request.data['method'] == 'Voters Card':
            verification_name = inclusive_voter_card(id_number)

        if verification_name['status'] == 400:
            return Response(verification_name)

        else:
            if is_similar(fullname, verification_name):
                instance.verification_completed = True
                instance.save()
            else:
                return Response(data={
                    "message": "Not Verified. Information MisMatch",
                    "status": 400}
                )

        return Response(status=200, data={"message": "Successfully Verified Account"})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.verification_completed:
            instance.verification_in_progress = True
        
        if request.data['id_front'] and request.data['id_back']:
            instance.id_front = request.data['id_front']
            instance.id_back = request.data['id_back']
            instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.save()
        return Response(serializer.data)


class UserLoginHistoryModelViewSet(ModelViewSet):
    model = UserLoginHistory
    serializer_class = UserLoginHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserLoginHistory.objects.filter(user=self.request.user)


class AdminUserModelViewSet(ModelViewSet):
    """ Admin Endpoints """
    model = User
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserModelSerializer

    @list_route(methods=['GET'], serializer_class=AdminUserModelSerializer)
    def verified_users(self, request):
        """ Get all verified accounts """
        verified_users = User.objects.filter(verification_completed=True)
        serializer = self.get_serializer(verified_users, many=True)
        return  Response(serializer.data)
    
    @list_route(methods=['GET'], serializer_class=AdminUserModelSerializer)
    def unverified_users(self, request):
        """ Get all verified accounts """
        unverified_users = User.objects.filter(verification_completed=False)
        serializer = self.get_serializer(unverified_users, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET'], serializer_class=AdminUserModelSerializer)
    def verification_requests(self, request, *args, **kwargs):
        """ Get all all accounts that have sent verification requests """
        verification_requests = User.objects.filter(verification_in_progress=True)
        serializer = self.get_serializer(verification_requests, many=True)
        return  Response(serializer.data)
    
    @list_route(methods=['GET'], serializer_class=AdminUserModelSerializer)
    def declined_requests(self, request, *args, **kwargs):
        """ Get all all accounts that have been denied verification """
        verification_requests = User.objects.filter(verification_in_progress=True)
        serializer = self.get_serializer(verification_requests, many=True)
        return  Response(serializer.data)

    @detail_route(methods=['POST', 'PUT'], serializer_class=AdminUserModelSerializer)
    def verify_account(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user.verification_completed = True
        user.verification_in_progress = False
        serializer = self.get_serializer(user)
        user.save()
        return Response(serializer.data)

    @detail_route(methods=['POST', 'PUT'], serializer_class=AdminUserModelSerializer)
    def decline_verification(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user.verification_in_progress = False
        serializer = self.get_serializer(user)
        user.save()
        return Response(serializer.data)


class UserAnalyticsModelViewSet(ModelViewSet):
    model = UserAnalytics
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserModelSerializer











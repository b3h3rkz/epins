from rest_framework.permissions import  BasePermission

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, object):
        return object.user == request.user

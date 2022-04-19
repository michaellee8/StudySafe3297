from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class HasEnterPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        return user.has_perm('can_enter_venue')


class HasExitPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        return user.has_perm('can_exit_venue')

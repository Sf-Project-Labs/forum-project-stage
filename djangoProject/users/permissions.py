from rest_framework.permissions import BasePermission


class IsStartup(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'startup'


class IsInvestor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'investor'

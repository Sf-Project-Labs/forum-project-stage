from rest_framework.permissions import BasePermission


class IsStartup(BasePermission):
    """
    Custom permission class to allow access only to users with the role 'startup'.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has the role 'startup'.

        Args:
            request: The HTTP request object.
            view: The view being accessed.

        Returns:
            bool: True if the user is authenticated and has the role 'startup', False otherwise.
        """
        return request.user.is_authenticated and request.user.role == 'startup'


class IsInvestor(BasePermission):
    """
    Custom permission class to allow access only to users with the role 'investor'.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has the role 'investor'.

        Args:
            request: The HTTP request object.
            view: The view being accessed.

        Returns:
            bool: True if the user is authenticated and has the role 'investor', False otherwise.
        """
        return request.user.is_authenticated and request.user.role == 'investor'

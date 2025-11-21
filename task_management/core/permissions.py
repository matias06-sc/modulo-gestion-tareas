from rest_framework.permissions import BasePermission

class IsAdminOrProductOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET','HEAD','OPTIONS'):
            return True
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            return request.user.groups.filter(name__in=['admin','product_owner','developer']).exists()
        return False

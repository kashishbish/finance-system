from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    
    message = 'Only admin users can perform this action.'

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsAnalystOrAdmin(BasePermission):
    
    message = 'Only analyst or admin users can perform this action.'

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['analyst', 'admin']
        )


class IsOwnerOrAdmin(BasePermission):
    
    message = 'You do not have permission to access this record.'

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin' or
            obj.user == request.user
        )
from rest_framework import permissions


class IsGroupAdminPermission(permissions.BasePermission):
    """
    Permission check for group admin permission
    """

    def has_object_permission(self, request, view, group):
        return request.user == group.created_by


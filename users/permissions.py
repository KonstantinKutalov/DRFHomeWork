from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.groups.filter(name='Moderators').exists()

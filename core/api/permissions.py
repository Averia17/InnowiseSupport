from rest_framework import permissions


class IsOwnerOrSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user.profile


class IsSupport(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.service_type == '2'

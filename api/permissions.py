"""
Custom Permissions for Spiritual G-Code API.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class HasDailyGCodeEnabled(permissions.BasePermission):
    """
    Check if user has daily G-Code calculations enabled.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.daily_gcode_enabled

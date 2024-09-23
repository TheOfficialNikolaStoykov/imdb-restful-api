from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    Custom permission that allows read-only access for all users, but write access only for admin users.
    """

    def has_permission(self, request, view):
        """
        Grant permission if the request method is safe (read-only) or if the user is an admin.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)


class IsReviewUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission that allows read-only access to all users, but write access only to the reviewer who created the review.
    """

    def has_object_permission(self, request, view, obj):
        """
        Grant permission if the request method is safe or if the user is the review's creator.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.reviewer == request.user
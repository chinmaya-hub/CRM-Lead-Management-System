from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Admin users can perform all actions.
    Authenticated non-admin users can read data only.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser or user.is_staff:
            return True

        return request.method in SAFE_METHODS


class IsAdminOrAssignedSalesperson(BasePermission):
    """
    Admin users can access all leads.
    Salespersons can access only their assigned leads.
    """

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and (
                user.is_superuser
                or user.is_staff
                or user.groups.filter(name='Salesperson').exists()
            )
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser or user.is_staff:
            return True

        return (
            obj.assigned_to_id == user.id
            and user.groups.filter(name='Salesperson').exists()
        )
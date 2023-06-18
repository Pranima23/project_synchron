from rest_framework import permissions
      

class IsSMorReadOnlyPermissions(permissions.BasePermission):
    """
    A permission for read/write operations where 
    only superuser or SM is allowed to write
    and other authenticated members can only read
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        required_group = 'Scrum Master'
        return request.user.groups.filter(name=required_group).exists() or request.user.is_superuser
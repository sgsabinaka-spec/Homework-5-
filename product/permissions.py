from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Правила модератора:
    1. is_staff = True
    2. Запрещен POST (создание)
    3. Разрешены GET, PUT, PATCH, DELETE (просмотр, изменение, удаление)
    """

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated and request.user.is_staff):
            return False
        
        if request.method == 'POST':
            return False
            
        return True

    def has_object_permission(self, request, view, obj):
        # return obj.owner != request.user
        
        return True
from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """Права доступа: только автор или админ может изменять/удалять."""
    
    def has_object_permission(self, request, view, obj):
        # Для безопасных методов (GET, HEAD, OPTIONS) - доступ есть
        if request.method in permissions.SAFE_METHODS:
            # Черновики видны только автору и админу
            if obj.status == 'DRAFT':
                return obj.creator == request.user or request.user.is_staff
            return True
        
        # Изменять/удалять может только автор или админ
        return obj.creator == request.user or request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """Для действий, требующих полного владения объектом."""
    
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user.is_staff
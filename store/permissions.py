from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    
    
class ViewCustomerHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        my_perm = request.user.has_perm('store.view_history')
        return request.user.has_perm('store.view_history')
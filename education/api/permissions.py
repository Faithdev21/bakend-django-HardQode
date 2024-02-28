from rest_framework import permissions

from products.models import Access


class HasAccessToProduct(permissions.BasePermission):
    """
    Пермишен, позволяющий доступ к уроку только если пользователь имеет доступ к соответствующему продукту.
    """
    def has_permission(self, request, view):
        product_id = view.kwargs.get('product_id')
        return Access.objects.filter(product_id=product_id, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        return Access.objects.filter(product=obj.product, user=request.user).exists()


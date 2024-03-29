from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AccessViewSet, LessonViewSet, ProductViewSet

router = DefaultRouter()

router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('products/<int:pk>/grant_access/', AccessViewSet.as_view(
        {'post': 'grant_access'}), name='grant_access'),
    path('products/<int:product_id>/lessons/', LessonViewSet.as_view(
        {'get': 'list'})),
    path('', include(router.urls))
]

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import HasAccessToProduct
from api.serializers import (AccessSerializer, LessonSerializer,
                             ProductSerializer)
from products.models import Access, Lesson, Product, User
from products.signals import access_granted


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(start_date__gt=timezone.now())
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = (HasAccessToProduct,)

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Lesson.objects.filter(product_id=product_id)


class AccessViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['post'])
    def grant_access(self, request, pk=None) -> Response:
        product = get_object_or_404(Product, pk=pk)
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        access, created = Access.objects.get_or_create(
            product=product,
            user=user
        )
        serializer = AccessSerializer(access)

        access_granted.send(sender=self.__class__, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

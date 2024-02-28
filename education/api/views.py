from django.utils import timezone
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from api.permissions import HasAccessToProduct
from products.models import Access, Product, Lesson, User, Group
from products.views import distribute_users_to_groups
from api.serializers import AccessSerializer, ProductSerializer, LessonSerializer


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
    def grant_access(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        access, created = Access.objects.get_or_create(product=product, user=user)
        serializer = AccessSerializer(access)

        try:
            group = product.groups.annotate(num_students=Count('students')).filter(
                num_students__lt=product.max_group_users).first()
            group.students.add(user)
        except Group.DoesNotExist:
            raise ValidationError("Все группы заполнены.")

        if product.start_date > timezone.now():
            distribute_users_to_groups(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

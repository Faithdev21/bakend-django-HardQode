from rest_framework import serializers

from products import constants
from products.models import Access, Lesson, Product, User


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    groups_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'start_date',
            'cost', 'lessons_count', 'students_count',
            'groups_fill_percentage', 'purchase_percentage'
        )

    def get_lessons_count(self, obj) -> int:
        """Количество уроков в продукте."""
        return obj.lessons.count()

    def get_students_count(self, obj) -> int:
        """Количество студентов, имеющих доступ к продукту."""
        return obj.access_set.count()

    def get_groups_fill_percentage(self, obj) -> int:
        """% наполняемости групп продукта."""
        total_groups = obj.groups.count()
        if total_groups == 0:
            return 0
        total_students = sum(
            group.students.count() for group in obj.groups.all()
        )
        max_group_students = obj.max_group_users * total_groups
        fill_percentage = ((total_students / max_group_students)
                           * constants.PERCENTAGE)
        return round(fill_percentage)

    def get_purchase_percentage(self, obj) -> int:
        """% приобретения продукта."""
        total_users = User.objects.count()
        if total_users == 0:
            return 0
        purchase_percentage = ((obj.access_set.count() / total_users)
                               * constants.PERCENTAGE)
        return round(purchase_percentage)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'link',)


class AccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Access
        fields = '__all__'

import itertools

from django.db.models import Count
from rest_framework.exceptions import ValidationError


def distribute_users_to_groups(product):
    """Распределение студентов по группам."""
    groups = product.groups.annotate(
        num_students=Count('students')
    ).order_by('num_students')

    users_without_group = product.access_set.exclude(
        user__in=product.groups.values_list('students__pk', flat=True)
    )
    group_cycle = itertools.cycle(groups)

    for user_access in users_without_group:
        group = next(group_cycle)

        if group.students.count() < product.max_group_users:
            group.students.add(user_access.user)
        else:
            raise ValidationError("Все группы уже заполнены")

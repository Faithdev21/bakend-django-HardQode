import itertools

from django.db.models import Count


def distribute_users_to_groups(product):
    groups = product.groups.annotate(num_students=Count('students')).order_by('num_students')

    users_without_group = product.access_set.exclude(user__in=product.groups.values_list('students__pk', flat=True))
    group_cycle = itertools.cycle(groups)

    for user_access in users_without_group:
        group = next(group_cycle)
        group.students.add(user_access.user)

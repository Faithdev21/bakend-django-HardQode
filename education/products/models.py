from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Product(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Автор",
    )
    title = models.CharField(
        "Название продукта",
        max_length=255,
        unique=True,
    )
    start_date = models.DateTimeField(
        "Дата старта",
    )
    cost = models.DecimalField(
        "Стоимость продукта",
        max_digits=10,
        decimal_places=2
    )
    min_group_users = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    max_group_users = models.PositiveIntegerField(
        default=100,
        validators=[MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.creator} - {self.title} ({self.cost})"

    class Meta:
        ordering = ('id',)
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Lesson(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="lessons",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
    )
    name = models.CharField(
        "Название урока",
        max_length=255,
        unique=True,
    )
    link = models.URLField(
        "Ссылка на видео"
    )

    def __str__(self):
        return f"{self.product.title} - {self.name}"

    class Meta:
        ordering = ('id',)
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Group(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="groups",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
    )
    name = models.CharField(
        "Название группы",
        max_length=255,
        unique=True,
    )

    students = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.product.title}: Группа - {self.name}"

    class Meta:
        ordering = ('id',)
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Access(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_access'
            ),
        ]

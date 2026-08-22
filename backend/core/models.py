from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


class User(AbstractUser):
    pass


class ClearanceLevel(models.Model):
    number = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name='уровень'
    )

    class Meta:
        ordering = ["number"]
        verbose_name = 'Уровень Допуска'
        verbose_name_plural = 'Уровни Допуска'

    @property
    def name(self):
        return f'{self.number}-У.Д.'

    def __str__(self) -> str:
        return self.name

    
class Template(models.Model):
    class Type(models.TextChoices):
        DOCUMENT = 'document', 'Документ'
        RESEARCH = 'research', 'Исследование'

    type = models.CharField(
        max_length=16,
        choices=Type.choices,
        verbose_name='тип'
        )
    name = models.CharField(
        max_length=128,
        verbose_name='название'
        )
    version = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='версия'
        )
    schema = models.JSONField(
        verbose_name='схема'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='активен'
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создано'
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='обновлено'
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['type', 'name', 'version'],
                name = 'template_unique_version',
            ),
            models.UniqueConstraint(
                fields=['type', 'name'],
                condition=Q(is_active=True),
                name='template_unique_active_type_name',
            )
        ]
        verbose_name='шаблон'
        verbose_name_plural='шаблоны'

    def __str__(self) -> str:
        return f"{self.name} v{self.version}"


class BaseApproval(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        APPROVED = 'approved', 'Согласовано'
        REJECTED = 'rejected', 'Отклонено'

    approver = models.ForeignKey(
        'employee.Employee',
        on_delete=models.PROTECT,
        related_name='%(class)s_approvals',
        verbose_name='утверждающий'
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='статус'
        )
    comment = models.TextField(
        blank=True,
        default='',
        max_length=10240,
        verbose_name='комментарий'
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создано'
        )
    decided_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='решено'
        )

    class Meta:
        abstract = True


class BaseContent(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='название'
    )
    content = models.JSONField(
        default=dict,
        verbose_name='содержание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='обновлено'
    )

    class Meta:
        abstract=True
from django.db import models

class Template(models.Model):
    class Type(models.TextChoices):
        DOCUMENT = 'document', 'Документ'
        RESEARCH = 'research', 'Исследование'

    type = models.CharField(max_length= 16)
    name = models.CharField(max_length=128)
    version = models.PositiveSmallIntegerField(default=1)
    schema = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['type', 'name', 'version'],
                name = 'template_unique_version',
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} v {self.version}"


class BaseApproval(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        APPROVED = 'approved', 'Согласовано'
        REJECTED = 'rejected', 'Отклонено'

    approver = models.ForeignKey(
        'employee.Employee',
        on_delete=models.PROTECT,
        related_name='%(class)s_approvals',
    )
    status = models.CharField(max_length=16, choices=Status, default=Status.PENDING)
    comment = models.CharField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True
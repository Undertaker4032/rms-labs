from django.db import models
from core.models import BaseContent, BaseApproval, Template
from django.db.models import Q


class Document(BaseContent):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        ON_REVIEW = 'on_review', 'На согласовании'
        APPROVED = 'approved', 'Согласован'
        REJECTED = 'rejected', 'Отклонен'
        PUBLISHED = 'published', 'Опубликован'
        ARCHIVED = 'archived', 'В архиве'

    template = models.ForeignKey(
        'core.Template',
        on_delete=models.PROTECT,
        limit_choices_to={'type': Template.Type.DOCUMENT.value},
        related_name='documents',
        verbose_name='шаблон'
    )
    author = models.ForeignKey(
        'employee.Employee',
        on_delete=models.PROTECT,
        related_name='documents',
        verbose_name='автор'
    )
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='статус'
    )
    required_clearance = models.ForeignKey(
        'core.ClearanceLevel',
        on_delete=models.PROTECT,
        related_name='documents',
        verbose_name='требуемый У.Д.'
    )

    class Meta:
        indexes = [
            models.Index(
                fields=['status', 'required_clearance']
            )]
        permissions = [
            ('submit_document', 'Can submit document for review'),
            ('review_document', 'Can review document'),
            ('publish_document', 'Can publish document'),
        ]
        verbose_name='документ'
        verbose_name_plural='документы'

    def __str__(self) -> str:
        return self.title


class DocumentApproval(BaseApproval):
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
        related_name='approvals',
        verbose_name='документ'
    )

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['document', 'approver'],
                condition=Q(status=BaseApproval.Status.PENDING),
                name='unique_pending_document_approver'
            )]
        verbose_name='утверждение документа'
        verbose_name_plural='утверждения документов'

    def __str__(self) -> str:
        return f'{self.document} — {self.approver} ({self.get_status_display()})'
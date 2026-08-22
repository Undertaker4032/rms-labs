from django.db import models
from core.models import BaseContent, BaseApproval, Template
from django.db.models import Q


class Research(BaseContent):
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Планируется'
        IN_PROGRESS = 'in_progress', 'В процессе'
        COMPLETED = 'completed', 'Завершено'
        FROZEN = 'frozen', 'Заморожено'

    template = models.ForeignKey(
        'core.Template',
        on_delete=models.PROTECT,
        limit_choices_to={'type': Template.Type.RESEARCH.value},
        related_name='research',
        verbose_name='шаблон'
    )
    lead = models.ForeignKey(
        'employee.Employee',
        on_delete=models.PROTECT,
        related_name='led_research',
        verbose_name='ведущий'
    )
    team = models.ManyToManyField(
        'employee.Employee',
        related_name= 'team_research',
        blank=True,
        verbose_name='участники'
    )
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name='статус'
    )
    required_clearance = models.ForeignKey(
        'core.ClearanceLevel',
        on_delete=models.PROTECT,
        related_name='researches',
        verbose_name='требуемый У.Д.'
    )

    class Meta:
        indexes = [
            models.Index(
                fields=['status', 'required_clearance']
            )]
        verbose_name='исследование'
        verbose_name_plural='исследования'

    def __str__(self) -> str:
        return self.title


class ResearchApproval(BaseApproval):
    research = models.ForeignKey(
        'Research',
        on_delete=models.CASCADE,
        related_name='approvals',
        verbose_name='исследование'
    )

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['research', 'approver'],
                condition=Q(status=BaseApproval.Status.PENDING),
                name='unique_pending_research_approver'
            )]
        verbose_name='утверждение исследования'
        verbose_name_plural='утверждения исследований'

    def __str__(self) -> str:
        return f'{self.research} — {self.approver} ({self.get_status_display()})'
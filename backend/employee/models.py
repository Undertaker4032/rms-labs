from django.conf import settings
from django.db import models


class Cluster(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='название'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'кластер'
        verbose_name_plural = 'кластеры'

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    cluster = models.ForeignKey(
        'Cluster',
        on_delete=models.PROTECT,
        related_name='departments',
        verbose_name='кластер'
    )
    name = models.CharField(
        max_length=128,
        verbose_name='название'
    )

    class Meta:
        ordering = ['cluster__name', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['cluster', 'name'],
                name='department_unique_per_cluster'
                )]
        verbose_name = 'департамент'
        verbose_name_plural = 'департаменты'

    def __str__(self) -> str:
        return f'{self.cluster.name} -> {self.name}'


class Division(models.Model):
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        related_name='divisions',
        verbose_name='департамент'
    )
    name = models.CharField(
        max_length=128,
        verbose_name='название'
    )

    class Meta:
        ordering = ['department__name', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['department', 'name'],
                name='division_unique_per_department'
                )]
        verbose_name = 'отдел'
        verbose_name_plural = 'отделы'

    def __str__(self) -> str:
        return f"{self.department.name} -> {self.name}"


class Position(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='название'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'должность'
        verbose_name_plural = 'должности'

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='employee',
        verbose_name='пользователь'
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name='фамилия'
    )
    first_name = models.CharField(
        max_length=64,
        verbose_name='имя'
    )
    middle_name = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name='отчество'
    )
    clearance_level = models.ForeignKey(
        'core.ClearanceLevel',
        on_delete=models.PROTECT,
        related_name='employees',
        verbose_name='Уровень Допуска'
    )
    division = models.ForeignKey(
        'Division',
        on_delete=models.PROTECT,
        related_name='employees',
        verbose_name='отдел'
    )
    position = models.ForeignKey(
        'Position',
        on_delete=models.PROTECT,
        related_name='employees',
        verbose_name='должность'
    )
    photo = models.ImageField(
        upload_to='employees/photos/',
        null=True,
        blank=True,
        verbose_name='фото'
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
        indexes = [models.Index(
            fields=['last_name', 'first_name']
            )]
        ordering = ['last_name', 'first_name']
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

    @property
    def full_name(self) -> str:
        return ' '.join(
            p for p in (self.last_name, self.first_name, self.middle_name) if p
            )

    @property
    def department(self) -> Department:
        return self.division.department

    @property
    def cluster(self) -> Cluster:
        return self.division.department.cluster

    def __str__(self) -> str:
        return self.full_name
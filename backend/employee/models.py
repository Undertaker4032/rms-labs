from django.contrib.auth.models import User
from django.db import models

class ClearanceLevel(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["number"]

    @property
    def name(self):
        return f'{self.number}-У.Д.'

    def __str__(self) -> str:
        return self.name


class Cluster(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name

class Department(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.PROTECT, related_name='departments')
    name = models.CharField(max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cluster', 'name'], name='department_unique_per_cluster'),
        ]

    def __str__(self) -> str:
        return f'{self.cluster.name} -> {self.name}'


class Division(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='divisions')
    name = models.CharField(max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department', 'name'], name='division_unique_per_department'),
        ]

    def __str__(self) -> str:
        return f"{self.department} -> {self.name}"

class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='employee')
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True, default='')
    clearance_level = models.ForeignKey(ClearanceLevel, on_delete=models.PROTECT, related_name='employees')
    division = models.ForeignKey(Division, on_delete=models.PROTECT, related_name='employees')
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name='employees')
    photo = models.ImageField(upload_to='employees/photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['last_name', 'first_name'])]

    @property
    def full_name(self) -> str:
        return ' '.join(p for p in (self.last_name, self.first_name, self.middle_name) if p)

    @property
    def department(self) -> Department:
        return self.division.department

    @property
    def cluster(self) -> Cluster:
        return self.division.department.cluster

    def __str__(self) -> str:
        return self.full_name
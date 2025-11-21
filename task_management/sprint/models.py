from django.db import models
from django.utils import timezone
import uuid

def default_progreso():
    return {"done": 0, "total": 0}

def default_checklist():
    return []

class Member(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    iniciales = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=7, blank=True)  # #RRGGBB

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

class SprintColumn(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    titulo = models.CharField(max_length=120)
    orden = models.IntegerField(default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"col-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)


class Card(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    titulo = models.CharField(max_length=160)
    puntos = models.IntegerField(default=0)
    tags = models.JSONField(default=list, blank=True)
    owner = models.CharField(max_length=8, blank=True)  # iniciales del Member

    progreso = models.JSONField(default=default_progreso)

    fecha = models.DateField(null=True, blank=True)

    checklist = models.JSONField(default=default_checklist, blank=True)

    storyId = models.CharField(max_length=32, null=True, blank=True)

    column = models.ForeignKey(SprintColumn, related_name='cards', on_delete=models.CASCADE)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"card-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

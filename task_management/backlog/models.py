from django.db import models
from django.utils import timezone
import uuid

PRIORITY_CHOICES = [('Crítica','Crítica'),('Alta','Alta'),('Media','Media'),('Baja','Baja')]
STATE_CHOICES = [('Lista','Lista'),('En revisión','En revisión'),('Hecha','Hecha')]

class Story(models.Model):
    id = models.CharField(max_length=32, primary_key=True)  # p.ej. "US-001" o hacer UUID
    titulo = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    prioridad = models.CharField(max_length=16, choices=PRIORITY_CHOICES)
    estado = models.CharField(max_length=20, choices=STATE_CHOICES, default='Lista')
    etiqueta = models.CharField(max_length=64, blank=True)
    puntos = models.IntegerField(null=True, blank=True)
    autor = models.CharField(max_length=100, blank=True)
    listaParaSprint = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    @property
    def estimada(self):
        return self.puntos is not None

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"US-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

class Template(models.Model):
    code = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=160)
    desc = models.TextField(blank=True)
    tag = models.CharField(max_length=64)
    proyecto = models.CharField(max_length=64)
    favorito = models.BooleanField(default=False)
    clones = models.IntegerField(default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"TPL-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

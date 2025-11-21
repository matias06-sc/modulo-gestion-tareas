from rest_framework import serializers
from .models import Story, Template
from django.core.validators import MinValueValidator

class StorySerializer(serializers.ModelSerializer):
    estimada = serializers.BooleanField(read_only=True)
    class Meta:
        model = Story
        fields = '__all__'
    def validate_titulo(self, v):
        if len(v) < 3 or len(v) > 160:
            raise serializers.ValidationError("Título debe tener 3-160 caracteres")
        return v
    def validate_puntos(self, v):
        if v is not None and v < 0:
            raise serializers.ValidationError("Puntos debe ser >= 0")
        return v

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'
    def validate_title(self, v):
        if not v:
            raise serializers.ValidationError("Title requerido")
        return v

from rest_framework import serializers
from .models import Member, SprintColumn, Card

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class SprintColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprintColumn
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
    def validate_titulo(self, v):
        if len(v) < 3 or len(v) > 160:
            raise serializers.ValidationError("Título debe tener 3-160 caracteres")
        return v
    def validate_puntos(self, v):
        if v < 0:
            raise serializers.ValidationError("Puntos debe ser >= 0")
        return v
    
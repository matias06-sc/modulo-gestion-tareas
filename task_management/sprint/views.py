from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Member, SprintColumn, Card
from .serializers import MemberSerializer, SprintColumnSerializer, CardSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'id'

class SprintColumnViewSet(viewsets.ModelViewSet):
    queryset = SprintColumn.objects.all().order_by('orden')
    serializer_class = SprintColumnSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['put'])
    def save_columns(self, request):
        # Persistencia transaccional: recibir array de columnas con sus cards
        from django.db import transaction
        data = request.data
        with transaction.atomic():
            for idx, col in enumerate(data):
                c, _ = SprintColumn.objects.update_or_create(id=col.get('id'), defaults={'titulo':col['titulo'], 'orden': idx})
                # opcional: actualizar cards aquí
        return Response({'status':'ok'})

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all().order_by('-createdAt')
    serializer_class = CardSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        # body: { "columnId": "...", "card": { ... } }
        column_id = request.data.get('columnId')
        card_data = request.data.get('card', {})
        try:
            column = SprintColumn.objects.get(id=column_id)
        except SprintColumn.DoesNotExist:
            return Response({"detail":"column not found"}, status=status.HTTP_404_NOT_FOUND)
        card_data['column'] = column.id
        serializer = self.get_serializer(data=card_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(column=column)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def move(self, request, id=None):
        fromColumn = request.data.get('fromColumnId')
        toColumn = request.data.get('toColumnId')
        try:
            card = self.get_object()
            target = SprintColumn.objects.get(id=toColumn)
            card.column = target
            card.save()
            # emitir evento CardMoved (aqui solo response)
            return Response({"status":"moved"})
        except SprintColumn.DoesNotExist:
            return Response({"detail":"destination column not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Story, Template
from .serializers import StorySerializer, TemplateSerializer
from django.db.models import Count

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-createdAt')
    serializer_class = StorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id','titulo','descripcion','etiqueta','autor']
    ordering_fields = ['createdAt','puntos','prioridad']
    lookup_field = 'id'

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = self.queryset.count()
        puntos = self.queryset.aggregate(total_puntos=models.Sum('puntos'))['total_puntos'] or 0
        listasSprint = self.queryset.filter(listaParaSprint=True).count()
        sinEstimar = self.queryset.filter(puntos__isnull=True).count()
        return Response({'total': total, 'puntos': puntos, 'listasSprint': listasSprint, 'sinEstimar': sinEstimar})

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all().order_by('-createdAt')
    serializer_class = TemplateSerializer
    lookup_field = 'code'

    @action(detail=True, methods=['post'])
    def duplicate(self, request, code=None):
        template = self.get_object()
        template.clones += 1
        template.save()
        new = Template.objects.create(
            code=f"{template.code}-COPY-{template.clones}",
            title=template.title,
            desc=template.desc,
            tag=template.tag,
            proyecto=template.proyecto,
            favorito=False,
            clones=0
        )
        serializer = self.get_serializer(new)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_favorito(self, request, code=None):
        t = self.get_object()
        t.favorito = not t.favorito
        t.save()
        return Response(self.get_serializer(t).data)

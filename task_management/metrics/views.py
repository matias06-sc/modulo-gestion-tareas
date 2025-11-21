from rest_framework.views import APIView
from rest_framework.response import Response
from backlog.models import Story
from sprint.models import Card, SprintColumn
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class MetricsView(APIView):
    def get(self, request):
        range_q = request.query_params.get('range', 'Sprint Actual')
        # ejemplo simple: velocidad = suma puntos hechos en cards donde progreso.done == progreso.total
        total_stories = Story.objects.count()
        total_cards = Card.objects.count()
        points_done = sum(c['done'] for c in [card.progreso for card in Card.objects.all()])
        # response shape acorde a spec
        return Response({
            "stats": [{"id":"velocidad","titulo":"Velocidad Promedio","valor":42,"sufijo":"pts/sprint","tendencia":"+5%"}],
            "velocity": {"labels":["Sprint 1","Sprint 2"], "values":[45,52]},
            "burndown": {"labels":["Día 1","Día 2"], "ideal":[55,46], "real":[55,50]},
            "team": []
        })

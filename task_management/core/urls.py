from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from backlog.views import StoryViewSet, TemplateViewSet
from sprint.views import MemberViewSet, SprintColumnViewSet, CardViewSet
from metrics import views as metrics_views

router = routers.DefaultRouter()
router.register(r'backlog/stories', StoryViewSet, basename='stories')
router.register(r'repo/templates', TemplateViewSet, basename='templates')
router.register(r'sprint/members', MemberViewSet, basename='members')
router.register(r'sprint/columns', SprintColumnViewSet, basename='columns')
router.register(r'sprint/cards', CardViewSet, basename='cards')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/metrics/', metrics_views.MetricsView.as_view(), name='metrics'),
    path('api/auth/', include('rest_framework.urls')),  # login for browsable API
    # JWT endpoints (simplejwt)
    path('api/token/', metrics_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', metrics_views.TokenRefreshView.as_view(), name='token_refresh'),
]

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from core.api.views import TicketViewSet

router = SimpleRouter()

router.register('tickets', TicketViewSet, basename='tickets')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token-verify')
]
urlpatterns += router.urls

from django.urls import path
from .views import ParticipantCreateView, ParticipantListView, \
ParticipantValidateView, UpdatePayementView, verify_email
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/participants/create/', ParticipantCreateView.as_view(), name='participant-create'),
    path('api/participants/', ParticipantListView.as_view(), name='participant-list'),
    path('api/participants/validate/<int:pk>/', ParticipantValidateView.as_view(), name='participant-validate'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/participants/validpay/',UpdatePayementView.as_view(), name='pay-inscription'),
    path('api/verifyemail/', verify_email, name = 'verify_email') 
]
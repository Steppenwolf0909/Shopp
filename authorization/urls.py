from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
from . import views
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send_code/', views.SendCodeView.as_view(), name='send_authorizatin_code'),
    path('check_mail/', views.CheckMail.as_view(), name='send_check_code'),
    path('confirm_mail/', views.ConfirmMail.as_view(), name='confirm_mail')
]
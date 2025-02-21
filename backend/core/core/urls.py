"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts .views import registerview, loginview
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from emotion.views import DetectEmotionView
from emotion.views import PredictMovementView
from emotion.views import AlphaPowerView

urlpatterns = [
    path('api/register/', registerview.as_view()),
    path('api/login/', loginview.as_view()),
    path('classify-and-send/', PredictMovementView.as_view()),
    # path('api/profile/', Profileview.as_view()),
    path('api/emotion/', DetectEmotionView.as_view()),
    path('api/alpha-power/', AlphaPowerView.as_view(), name='alpha-power'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]
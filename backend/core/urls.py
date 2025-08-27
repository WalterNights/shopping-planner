from django.contrib import admin
from django.urls import path, include
from users.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/shopping/', include('shopping.urls')),
    path('api/token/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user',views.UserViewSet,basename='user')



urlpatterns=[
    path('',views.getRoutes),
    path('token/',views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update-image/', views.UpdateProfileImageView.as_view(), name='profile'),
    path('', include(router.urls)),
    path('user_search/<str:key>/',views.search_user,name='search_user')
    
]

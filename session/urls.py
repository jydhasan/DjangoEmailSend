from session import views
from django.urls import path
urlpatterns = [
    path('login/', views.loginuser),
    path('logout/', views.logoutuser),
    path('signup/', views.registration),
    path('password/', views.changepassword),
]

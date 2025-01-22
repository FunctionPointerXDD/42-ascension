from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserDetailView 

urlpatterns = [
    path('user/', UserDetailView.as_view()),
    #path('user/<int:pk>/', views.UserDetail.as_view()),
    path('user/friend/', UserDetailView.Friends.as_view()),
    path('user/dashboard/', UserDetailView.DashBoard.as_view()),
]

# receive that { /users.json, /users.xml ... }
urlpatterns = format_suffix_patterns(urlpatterns)
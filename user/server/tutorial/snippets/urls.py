from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),
    # user -> snippet(admin_mod?)
    path('user/', views.SnippetList.as_view()),
    path('user/<int:pk>/', views.SnippetDetail.as_view()),

    # users -> usermod
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

# receive that { /users.json, /users.xml ... }
urlpatterns = format_suffix_patterns(urlpatterns)

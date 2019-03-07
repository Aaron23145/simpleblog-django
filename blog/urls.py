from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/auth/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='blog/auth/logout.html'
    ), name='logout'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('editorcp/', views.editorcp_index, name='editorcp'),
    path('editorcp/entries/new/', views.editorcp_create_entry, name='create_entry'),
]

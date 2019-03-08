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
    path('editorcp/entries/new/', views.EditorcpCreateEntry.as_view(), name='create_entry'),
    path('editorcp/entries/', views.EditorcpListEntries.as_view(), name='list_entries'),
    path('editorcp/entries/<int:pk>/', views.EditorcpEditEntry.as_view(), name='edit_entry'),
    path('editorcp/entries/<int:pk>/remove/', views.EditorcpDeleteEntry.as_view(), name='delete_entry'),
]

from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

AUTH_PATTERNS = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='blog/auth/logout.html'
    ), name='logout'),
    path('signup/', views.Signup.as_view(), name='signup'),
]

EDITORCP_PATTERNS = [
    path('', views.editorcp_index, name='editorcp'),
    path('entries/new/', views.EditorcpCreateEntry.as_view(), name='create_entry'),
    path('entries/', views.EditorcpListEntries.as_view(), name='list_entries'),
    path('entries/<int:pk>/', views.EditorcpEditEntry.as_view(), name='edit_entry'),
    path('entries/<int:pk>/remove/', views.EditorcpDeleteEntry.as_view(), name='delete_entry'),
]

app_name = 'blog'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('', include(AUTH_PATTERNS)),
    path('editorcp/', include(EDITORCP_PATTERNS)),
]

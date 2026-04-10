from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('book/<int:skill_id>/', views.book_skill, name='book_skill'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/bayani/', views.bayani_dashboard, name='bayani_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('subscribe/', views.subscribe, name='subscription'),
    # path('deleteaccount/', views.deleteaccount, name='delete_account'),
]
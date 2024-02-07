from django.urls import path
from users.views import *


urlpatterns = [
    path('create/', UserRegister.as_view(), name="register"),
    path('<int:pk>/update/', UserUpdate.as_view(), name="users_update"),
    path('<int:pk>/delete/', UserDelete.as_view(), name="users_delete"),
]

from django.urls import path
from .views import *

urlpatterns=[
    path('login/',Login.as_view(),name='login'),
    path('todo/',Todo.as_view(),name='todo'),
    path('todo/<int:id>/',Todo.as_view(),name='todo')
]
from rest_framework import serializers
from .models import *

class GetAllTodo(serializers.ModelSerializer):
    class Meta:
        model=TodoList
        fields = '__all__'

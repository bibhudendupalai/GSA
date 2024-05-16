from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import *
from .models import CustomeUser,TodoList


User=get_user_model()

# Create your views here.

class Login(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        if "username" not in request.data:
            Err="username not Given"
            return Response({"msg":"Username missing"},status=status.HTTP_401_UNAUTHORIZED)

        if "password" not in request.data:
            return Response({"msg":"Password missing"},status=status.HTTP_401_UNAUTHORIZED)       


        username=request.data["username"]
        password=request.data['password'].replace(" ","")

        if not  User.objects.filter(username=username).exists():
            return Response({"msg":"User Not exist"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            if authenticate(username=username, password=password):
                user = User.objects.get(username=username)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,"msg":"Login successfull"}, status=status.HTTP_200_OK)
                
        except:
            return Response({"msg":"Invalid"}, status=status.HTTP_401_UNAUTHORIZED)
 
class Todo(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        qu=TodoList.objects.filter(user=request.user)
        serialize=GetAllTodo(qu,many=True)
        return Response({"data":serialize.data})
    
    def post(self,request):
        data=request.data
        TodoList(user=request.user,title=data["data"],completed=True).save()
        dic={
            "id":TodoList.objects.filter(user=request.user).count()+1,
            "title":data["data"]
        }

        return Response({'data':dic})
    
    def put(self,request,id=None):
        print(request.data['data'],id)
        # try:
        TodoList.objects.filter(id=id,user=request.user).update(title=request.data['data'])
        return Response({"msg":"Data Updated"}, status=200)
        # except TodoList.DoesNotExist:
        #     return Response({'msg': 'Todo does not exist'}, status=404)

    def delete(self,request,id=None):
        todo=None
        try:
            todo = TodoList.objects.get(id=id).delete()
            return Response({'msg': 'Delete sucessful'}, status=200)
        except TodoList.DoesNotExist:
            return Response({'msg': 'Todo does not exist'}, status=404)

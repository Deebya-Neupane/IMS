from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import DepartmentSerializer, ResourceSerializer, UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import DjangoModelPermissions
from .permissions import CustomModelPermission
from django.contrib.auth.models import Group


# Create your views here.
class DepartmentView(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class ResourceView(GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get(self,request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data created!')
        else:
            return Response(serializer.errors)
        
class ResourceDetailView(GenericAPIView): 
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get(self,request,pk):
        try:
           queryset = Resource.objects.get(id=pk)
        except:
           return Response("Data not found!",status=status.HTTP_404_NOT_FOUND)   
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
           queryset = Resource.objects.get(id=pk)
        except:
           return Response("Data not found!",status=status.HTTP_404_NOT_FOUND)  
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Data updated!")
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
           queryset = Resource.objects.get(id=pk)
        except:
           return Response("Data not found!",status=status.HTTP_404_NOT_FOUND)  
        queryset.delete()
        return Response("Data deleted!")  

@api_view(['POST'])
@permission_classes([AllowAny,])
def register(request):    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        hash_password = make_password(password)
        a = serializer.save()
        a.password = hash_password
        a.save()
        return Response('User created!')
    else:
        return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([AllowAny,])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email,password=password)
    if user == None:
        return Response('Email or password is incorrect!')
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return Response(token.key)

@api_view(['GET'])
@permission_classes([AllowAny,])
def group_listing(request):
    group_objs = Group.objects.all()
    serializer = GroupSerializer(group_objs,many=True)
    return Response(serializer.data)






    

    

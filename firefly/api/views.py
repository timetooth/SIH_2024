from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import User
from .serializers import UserSerializer
# Create your views here.
def home(request):
    data = {'message': 'Hello, World!'}
    response = Response(data)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {}
    return response

@api_view(['GET'])
def user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)  # Serialize the queryset
    response = Response(serializer.data)
    return response
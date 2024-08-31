from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def home(request):
    data = {'message': 'This is the API testing route'}
    return Response(data)
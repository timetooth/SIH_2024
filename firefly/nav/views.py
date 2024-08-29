from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def test(request):
    data = {'message': 'Hello tester, This is the Navigation api testing route'}
    return Response(data)
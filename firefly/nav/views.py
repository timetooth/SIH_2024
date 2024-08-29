from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import PathFinder

@api_view(['GET'])
def test(request):
    data = {'message': 'Hello tester, This is the Navigation api testing route'}
    print(type(request.query_params.get('arr')))
    print(request.query_params.get('arr'))
    return Response(data)

@api_view(['POST'])
def navigate(request):
    grid = request.data.get('grid')
    goal_nodes = request.data.get('goal_nodes')
    entry = request.data.get('entry')
    fire = request.data.get('fire')
    print(grid, goal_nodes, entry, fire)
    try:
        path = PathFinder.path_finder(grid=grid, goal_nodes=goal_nodes, entry=entry, fire=fire)
    except Exception as e:
        return Response({'error': str(e)})
    res = {'path': path}
    return Response(res)
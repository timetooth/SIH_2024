from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from . import PathFinder
from . import models
from . import serializer
from . import simulate_fire
from datetime import datetime

@api_view(['GET','POST'])
def navigate(request):
    '''
    This function is used to navigate the user to the nearest fire exit, medical kit or extinguisher
    POST request:
    grid: 2D array, goal_nodes: 2D array, entry: touple and fire: 2D array
    GET request:
    send the id:int primary key of building,
    method:string method can be fire, med or extinguisher
    entry:2D array ([x,y]) current location of the user
    '''
    if request.method == 'POST':
        grid = request.data.get('grid')
        goal_nodes = request.data.get('goal_nodes')
        entry = request.data.get('entry')
        fire = request.data.get('fire')
        try:
            path = PathFinder.path_finder(grid=grid, goal_nodes=goal_nodes, entry=entry, fire=fire)
        except Exception as e:
            return Response({'error': str(e)})
        res = {'path': path}
        return Response(res)

    elif request.method == 'GET':
        id = request.query_params.get('id')
        method = request.query_params.get('method')
        entry = request.query_params.get('entry')
        if id is None or method is None or entry is None:
            err = {'error': 'id and/or method and/or entry are missing in the request. id is needed to fetch the building data and method can be fire, med or extinguisher (string) depending on where the user wants to go'}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        entry = entry.split(',')
        entry = [int(entry[0]), int(entry[1])]
        try:
            building = models.Building.objects.get(id=id)
        except models.Building.DoesNotExist:
            err = {'error': 'Building with the given id does not exist'}
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        grid = building.floor_map[0] # 0th floor
        fire = building.fire_matrix[0] # 0th floor
        grid, fire_exits, med_kits, extinguishers = PathFinder.map_handler(grid)
        if method == 'fire':
            goal_nodes = fire_exits
        elif method == 'med':
            goal_nodes = med_kits
        elif method == 'extinguisher':
            goal_nodes = extinguishers
        else:
            err = {'error': 'Invalid method, method can be fire, med or extinguisher (string) depending on where the user wants to go'}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        try:
            path = PathFinder.path_finder(grid=grid, goal_nodes=goal_nodes, entry = entry, fire= fire)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        res = {'path': path}
        return Response(res, status=status.HTTP_200_OK)

@api_view(['POST'])
def simulate(requests):
    '''
    This function is used to simulate the fire spread in the building
    GET request:
    ignite_cell:2D array ([x,y]) coordinates of the cell to ignite
    shape:2D array ([rows, cols]) shape of the grid
    steps:int number of keyframes
    alpha, beta, gamma: optional hypermeters,  range(0,1)
    warn_threshold:float threshold for warning, range(0,1)
    '''
    ignite_cell = requests.data.get('ignite_cell')
    shape = requests.data.get('shape')
    alpha = requests.data.get('alpha')
    beta = requests.data.get('beta')
    gamma = requests.data.get('gamma')
    steps = requests.data.get('steps')
    warn_threshold = requests.data.get('warn_threshold')
    if ignite_cell is None or shape is None or steps is None:
        err = {'error': 'ignite_cell, shape, steps are required parameters'}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
    alpha = 1 if alpha is None else alpha
    beta = 0.5 if beta is None else beta
    gamma = 0.1 if gamma is None else gamma
    warn_threshold = 0.8 if warn_threshold is None else warn_threshold
    cache = {}
    if f'{ignite_cell}{shape}{steps}' in cache:
        key_frames = cache[(ignite_cell, shape, steps)]
        return Response({'key_frames': key_frames})
    else:
        try:
            key_frames = simulate_fire.simulate_fire(ignite_cell, shape, alpha, beta, gamma, steps)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'grid': key_frames})

@api_view(['GET'])
def get_building(request):
    id = request.query_params.get('id')
    if id is None:
        err = {'error': 'id is required to fetch the building data'}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
    try:
        building = models.Building.objects.get(id=id)
    except models.Building.DoesNotExist:
        err = {'error': 'Building with the given id does not exist'}
        return Response(err, status=status.HTTP_404_NOT_FOUND)
    serialized = serializer.BuildingSerializer(building)
    return Response(serialized.data)

from . import dummy

@api_view(['GET'])
def test(request):
    path = dummy.path
    return Response({'path': path})
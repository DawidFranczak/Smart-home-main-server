from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serialized import AquaSerializer


@api_view(['GET'])
def getStairs(request, pk):
    settings = request.user.sensor_set.get(pk=pk).stairs
    serializer = AquaSerializer(settings, many=False)
    return Response(serializer.data)

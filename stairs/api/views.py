from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serialized import StairsSerializer


@api_view(['GET'])
def getStairs(request, pk):
    settings = request.user.device_set.get(pk=pk).stair
    serializer = StairsSerializer(settings, many=False)
    return Response(serializer.data)

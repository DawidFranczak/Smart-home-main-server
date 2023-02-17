from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serialized import AquaSerializer


@api_view(['GET'])
def getAqua(request, pk):
    settings = request.user.device_set.get(pk=pk).aqua
    serializer = AquaSerializer(settings, many=False)
    return Response(serializer.data)

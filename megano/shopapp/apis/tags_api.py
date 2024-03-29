from rest_framework.views import APIView
from rest_framework.response import Response
from shopapp.models import Tag
from shopapp.serializers import TagSerializer


class TagAPIView(APIView):
    """
    Tag lists
    """
    def get(self, request):
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)
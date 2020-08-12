from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class LoginUserView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        queryset = User.objects.filter(pk=request.user.id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


# Create your views here.

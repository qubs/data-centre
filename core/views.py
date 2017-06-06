from collections import OrderedDict

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from core.serializers import *


@api_view(["GET"])
def api_root(request, format=None):
    return Response(OrderedDict([
        ("climate", reverse("climate-api-root", request=request, format=format)),
        ("herbarium", reverse("herbarium-api-root", request=request, format=format)),

        ("users", reverse("user-list", request=request, format=format)),
    ]))


# User Views

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

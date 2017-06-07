from collections import OrderedDict

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api_herbarium.serializers import *


# API Root View

@api_view(["GET"])
def herbarium_api_root(request, format=None):
    return Response(OrderedDict([
        ("specimens", reverse("specimen-list", request=request, format=format)),
    ]))


class SpecimenList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all specimen entries.

    post:
    Create a new specimen entry in the database.
    """

    queryset = Specimen.objects.all()
    serializer_class = SpecimenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SpecimenDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Return information about a given station.
    """

    queryset = Specimen.objects.all()
    serializer_class = SpecimenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

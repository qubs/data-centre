from collections import OrderedDict

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from herbarium_data.serializers import *
from herbarium_data.filters import *


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
    filter_class = SpecimenFilter
    ordering_fields = '__all__'

    # Improve performance by not going through DRF serializer class.
    def list(self, request, *args, **kwargs):
        return Response(self.filter_queryset(self.get_queryset()).values(
            *getattr(self.get_serializer_class().Meta, 'fields', None))
        )


class SpecimenDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Return information about a given station.
    """

    queryset = Specimen.objects.all()
    serializer_class = SpecimenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

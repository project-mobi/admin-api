from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Regular http and json response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
# Http status codes
from rest_framework import status
from rest_framework import generics
# Api view decorator for better request/resonse handling
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Defined models
import restapi.models as models
import restapi.serializers as serializers

from django.contrib.auth.models import User

from rest_framework import permissions

from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action




# Refactor using viewsets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


# Refactor using viewset
class OrganisationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Organisation.objects.all()
    serializer_class = serializers.OrganisationSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   


class ServiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)



class DeploymentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Deployment.objects.all()
    serializer_class = serializers.DeploymentSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def new_deployments(self, request):
        new_deployments = models.Deployment.objects.all().order_by('-created')

        page = self.paginate_queryset(new_deployments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(new_deployments, many=True)
        return Response(serializer.data)



class LocationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProviderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MachineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Machine.objects.all()
    serializer_class = serializers.MachineSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
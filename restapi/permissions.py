import restapi.models as models
from rest_framework import permissions


class BelongsToOrganisation(permissions.IsAuthenticated):
    """
    Extend IsAuthenticated Class with object lever permissions
    """
    def has_object_permission(self, request, view, obj):

        if(type(obj) == type(models.Organisation())):
            return obj == request.user.organisation
        else:
            return obj.organisation == request.user.organisation


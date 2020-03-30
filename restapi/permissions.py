import restapi.models as models
from rest_framework import permissions


class BelongsToOrganisation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if(type(obj) == type(models.Organisation())):
            return obj == request.user.organisation
        else:
            return obj.organisation == request.user.organisation


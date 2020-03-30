from django_filters import rest_framework as filters
from restapi import models
from django.contrib.auth.models import AnonymousUser

import logging

logger = logging.getLogger('django.server')

class OrganisationFilter(filters.FilterSet):
    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        logger.info(parent.model.__dict__)
        if (type(user) != type(AnonymousUser())):
            if user.is_staff:
                    return parent
            else:
                if(type(parent.model) != type(models.Organisation())):
                    return parent.filter(organisation=user.organisation)
                else:
                    return parent.filter(id=user.organisation)
        else:
            return parent.filter(id=None)

from django_filters import rest_framework as filters
from restapi import models
from django.contrib.auth.models import AnonymousUser
from django.template.response import SimpleTemplateResponse

import logging

logger = logging.getLogger('django.server')

class BaseFilter(filters.FilterSet):
    """
    Filter Securing API requests based on organisation, except for superusers

    
    """
    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        if user.is_superuser:
                return parent
        else:
            if(type(parent.model) != type(models.Organisation())):
                return parent.filter(organisation=user.organisation)
            else:
                return parent.filter(id=user.organisation)

"""
Extend BaseFilter class with model / view specific filter fields
"""

class MachineFilter(BaseFilter):
    class Meta:
        model = models.Machine
        fields = ['type']
    

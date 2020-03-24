from rest_framework import serializers
from django.contrib.auth.models import User
from restapi.models import Organisation, Service, Deployment, Location, Provider, Machine

import re



class UserSerializer(serializers.HyperlinkedModelSerializer):
    services = serializers.HyperlinkedRelatedField(many=True, view_name="service-detail", read_only=True)

    class Meta:
        model = User
        fields = '__all__'

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    deployments = serializers.HyperlinkedRelatedField(many=True, view_name="deployment-detail", read_only=True)

    class Meta:
        model = Organisation
        fields = '__all__'
    

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    version = serializers.RegexField(r"v(([\d]{1,3})(.|$)){3}", required=True)
    development_stage = serializers.ChoiceField(choices=Service.DEV_STAGE_CHOICES)
    environment = serializers.ChoiceField(choices=Service.ENV_CHOICES)


    def validate_version(self, value):
        regex = r"^v(([\d]{1,3})(\.|$)){3}"
        
        if(not re.search(regex, value)):
            raise serializers.ValidationError("Version must follow this pattern v0.0.0")

        return value

    class Meta:
        model = Service
        fields = '__all__'


class DeploymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class MachineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'
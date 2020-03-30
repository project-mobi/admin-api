from rest_framework import serializers
#from django.contrib.auth.models import User
from restapi.models import Organisation, Service, Deployment, Location, Provider, Machine, User

import re



class UserSerializer(serializers.HyperlinkedModelSerializer):
    services = serializers.HyperlinkedRelatedField(many=True, view_name="service-detail", read_only=True)
    organisation = serializers.HyperlinkedRelatedField(view_name="organisation-detail", queryset=Organisation.objects.all())
    class Meta:
        model = User
        #fieldsList = User.objects.all()
        fields = ['url', 'services', 'organisation', 'username', 'password']
        #fields = '__all__'

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    deployments = serializers.HyperlinkedRelatedField(many=True, view_name="deployment-detail", read_only=True)
    machines = serializers.HyperlinkedRelatedField(many=True, view_name="machine-detail", read_only=True)
    users = serializers.HyperlinkedRelatedField(many=True, view_name="user-detail", read_only=True)
    
    class Meta:
        model = Organisation
        fields =['id', 'name', 'created', 'deployments', 'machines', 'users']
    

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
    def validate_ipv4(self, value):
        regex=r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\.|$)){4}"

        if(value != "" and not re.search(regex, value)):
            raise serializers.ValidationError("IPv4 Address is invalid")

        return value
    
    def validate_ipv6(self, value):
        regex=r"(([0-9a-f][0-9a-f][0-9a-f][0-9a-f]|[0-9a-f][0-9a-f][0-9a-f]|[0-9a-f][0-9a-f]|[0-9a-f])(\:|$)){8}"

        if(value != "" and not re.search(regex, value)):
            raise serializers.ValidationError("IPv6 Address is invalid")

        return value

    class Meta:
        model = Machine
        fields = '__all__'
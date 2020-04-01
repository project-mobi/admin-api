from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    organisation = models.ForeignKey(
        'Organisation',
        related_name='users',
        on_delete=models.CASCADE,
        default='c749d4a5-3d70-4661-a2c7-da1899c09282',
    )
    

class OrganisationManager(models.Manager):
    def get_by_natural_key(self, name, created):
        return self.get(**{self.model.NAME_FIELD: name, self.model.NAME_CREATED: created})


class Organisation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    #deployments = models.
    objects = OrganisationManager()

    class Meta:
        ordering = ['created']
        unique_together = [['name', 'created']]
    
    def __str__(self):
        return '%s - %s' % (self.name, self.created)




class ServiceManager(models.Manager):
    def get_by_natural_key(self, name, version):
        return self.get(name=name, version=version)


class Service(models.Model):
    DEV_STAGE_CHOICES = [('pre-alpha', 'pre-alpha'), ('alpha', 'alpha'), ('beta', 'beta'), ('stable', 'stable')]
    ENV_CHOICES = [('development', 'development'), ('testing', 'testing'), ('staging', 'staging'), ('production', 'production')]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    development_stage = models.CharField(
        max_length=10,
        choices=DEV_STAGE_CHOICES,
        default='beta'
    )
    version = models.CharField(
        max_length=12,
        help_text='"Version must follow this pattern v0.0.0"'
    )
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        'User',
        related_name='services',
        on_delete=models.CASCADE
    )
    
    active = models.BooleanField(default=False)
    source = models.URLField()
    website = models.URLField()
    environment = models.CharField(
        max_length=11,
        choices=ENV_CHOICES,
        default='staging'
    )

    objects = ServiceManager()

    class Meta:
        unique_together = [['name', 'version']]

    def __str__(self):
        return '%s - %s' % (self.name, self.version)

class Deployment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(
        'Organisation',
        on_delete=models.CASCADE,
        related_name='deployments'
    )

class Location(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=4)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    provider = models.ForeignKey(
        'Provider',
        on_delete=models.CASCADE
    )

    

class Provider(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s' % (self.name)

class Machine(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    provider = models.ForeignKey(
        'Provider',
        on_delete=models.CASCADE
    )
    ipv4 = models.CharField(max_length=15, blank=True)
    ipv6 = models.CharField(max_length=40, blank=True)
    hostname = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(
        "Organisation",
        default="426530a7-62a8-4234-b59a-c7d2baf2084c",
        on_delete=models.SET_DEFAULT,
        related_name='machines')
    type = models.CharField(
        max_length=6,
        choices=[('node', 'node'), ('master', 'master'), ('admin','admin')],
        default='node'
    )
    class Meta:
        ordering = ['created']
        #unique_together = [['name', 'created']]
    
    def __str__(self):
        return '%s - %s' % (self.provider, self.created)
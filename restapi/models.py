from django.db import models
import uuid

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
        'auth.User',
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
        on_delete=models.CASCADE
    )

class Location(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    

class Provider(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)

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
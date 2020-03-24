from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'organisations', views.OrganisationViewSet)
router.register(r'deployments', views.DeploymentViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'providers', views.ProviderViewSet)
router.register(r'machines', views.MachineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

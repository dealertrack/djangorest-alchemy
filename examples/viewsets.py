from djangorest_alchemy.managers import AlchemyModelManager
from djangorest_alchemy.viewsets import AlchemyModelViewSet

from models import Car, Part
from models import SessionMixin


class CarManager(SessionMixin, AlchemyModelManager):
    model_class = Car


class CarViewSet(AlchemyModelViewSet):
    manager_class = CarManager


class PartManager(SessionMixin, AlchemyModelManager):
    model_class = Part


class PartViewSet(AlchemyModelViewSet):
    manager_class = PartManager

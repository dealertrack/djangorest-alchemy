from djangorest_alchemy.managers import AlchemyModelManager
from djangorest_alchemy.viewsets import AlchemyModelViewSet

from models import Car, Part
from models import SessionMixin


class CarManager(SessionMixin, AlchemyModelManager):
    model_class = Car


class CarViewSet(AlchemyModelViewSet):
    '''
    /api/cars/?page=<num>
    /api/cars/?page=last
    /api/cars/?make=Toyota

    You can combine both filtering and pagination
    '''
    manager_class = CarManager
    paginate_by = 10


class PartManager(SessionMixin, AlchemyModelManager):
    model_class = Part


class PartViewSet(AlchemyModelViewSet):
    manager_class = PartManager

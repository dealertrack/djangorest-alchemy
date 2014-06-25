from djangorest_alchemy.managers import AlchemyModelManager
from djangorest_alchemy.viewsets import AlchemyModelViewSet
from djangorest_alchemy.mixins import ManagerActionMethodsMixin

from models import Car, Part
from models import SessionMixin


class CarManager(SessionMixin, AlchemyModelManager):
    model_class = Car
    action_methods = {'change_engine': ['GET', 'POST']}

    def change_engine(self, data, pk=None, **kwargs):
        return {'status': 'created'}


class CarViewSet(AlchemyModelViewSet, ManagerActionMethodsMixin):
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

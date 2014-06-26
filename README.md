djangorest-alchemy
===============================

A library to integrate the awesome frameworks Django REST Framework and SQLAlchemy

* Free software: MIT license
* Supports SQLAlchemy 0.7.8 and above


Features
--------

* Provides GET verb implementation for SQLAlchemy models
* List, filter and paginate multiple rows
* Fetch single object with nested objects as complete URIs
* Supports multiple primary keys
* Provides ability to use 'Manager' like classes to work with SQLAlchemy models
* Supports both Declarative and Classical styles

Install dependencies
--------------------
```
pip install -r requirements.txt
```

Run tests
---------
```
make test
```

Usage
------

**Getting Started**

Assuming you have a SQLAlchemy model defined as below::


    class DeclarativeModel(Base):
        __tablename__ = 'test_model'

        declarativemodel_id = Column(INTEGER, primary_key=True)
        field = Column(String)
        datetime = Column(DateTime, default=datetime.datetime.utcnow)
        floatfield = Column(Float)
        bigintfield = Column(BigInteger)
        child_model = relationship(ChildModel, uselist=False, primaryjoin=
                                  (declarativemodel_id == ChildModel.parent_id))



Define the 'manager' class to work on above model::

    class DeclarativeModelManager(SessionMixin, AlchemyModelManager):
        model_class = DeclarativeModel


*SessionMixin just provides a convenient way to initialize the SQLAlchemy session. You
can achieve the same by definining __init__ and setting ```self.session``` instance*


Define the Django REST viewset and specify the manager class::

    class DeclModelViewSet(AlchemyModelViewSet):
        manager_class = DeclarativeModelManager


Finally, register the routers as you would normally do using Django REST::

    viewset_router = routers.SimpleRouter()
    viewset_router.register(r'api/declmodels', DeclModelViewSet,
                            base_name='test-decl')


**Pagination**

Pagination works exactly like Django REST Framework (and Django). Provided your viewset
has the ```paginate_by``` field set, pass page number in querystring::

        class ModelViewSet(AlchemyModelViewSet):
            paginate_by = 25


* 5th page ```curl -v  http://server/api/declmodels/?page=5```
* Last page ```curl -v  http://server/api/declmodels/?page=last```
* First page ```curl -v  http://server/api/declmodels/```


**Filters**

Filters work exactly like Django REST Framework. Pass the field value pair in querystring.

```curl -v  http://server/api/declmodels/?field=value```


Advanced Usage
--------------


**Multiple primary keys**


To use some sort of identifier in the URI, the library tries to use the following
logic.

1. If a single primary key is found, use it! That was simple..
2. For multiple keys, try to find a field with convention 'model_id'
3. If not found, see if the model has 'pk_field' class variable
4. If not found, raise KeyNotFoundException


In addition, to support multiple primary keys which cannot be accomodated in the URI,
the viewset needs to override the ```get_other_pks``` method and return back
dictionary of primary keys. Example::

    class ModelViewSet(AlchemyModelViewSet):
        manager_class = ModelManager
        def get_other_pks(self, request):
            pks = {
                'pk1': request.META.get('PK1'),
                'pk2': request.META.get('PK2'),
            }
            return pks



**Manager factory**


The base AlchemyModelViewSet viewset provides a way to override the instantiation
of the manager. Example::

    class ModelViewSet(AlchemyModelViewSet):
        def manager_factory(self, *args, **kwargs):
            return ModelManager()


**Nested Models**


This library recommends using the drf-nested-routers for implementing nested child
models. Example::

    child_router = routers.NestedSimpleRouter(viewset_router, r'api/declmodels',
                                          lookup='declmodels')

For more details, refer to the drf-nested-routers documentation.


**Custom methods**

DRF allows to add custom methods other than the default list, retrieve, create, update and destroy
using the @action decorator. However, if you have managers, then you can simply provide action methods
on the manager and specify the action methods using `action_methods` field
The methods have to return back appropriate status per below map.


    STATUS_CODES = {
        'created': status.HTTP_201_CREATED,
        'updated': status.HTTP_200_OK,
        'accepted': status.HTTP_202_ACCEPTED
    }


    class MyManager(AlchemyModelManager):
        action_methods = {'do_something': ['POST']}

        def do_something(self, data, pk=None, **kwargs):
            # data is actual payload
            return {'status': 'created'}

    class ModelViewSet(AlchemyModelViewSet):
            manager_class = MyManager

```curl -X POST http://server/api/declmodels/1/do_something/```


Examples
--------

The examples folder demonstrates a real-world example using Cars and Parts as the object models.

Run the following command just as you would normally run a Django project:

```
cd examples
python manage.py runserver --settings=settings
```

Then type the following in your favorite browser:

```
http://localhost/api/cars/
```
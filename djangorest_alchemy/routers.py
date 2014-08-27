from rest_framework.routers import DefaultRouter
from rest_framework.routers import Route


class ReadOnlyRouter(DefaultRouter):
    """
    A router for read-only APIs, which USES trailing slashes.
    """
    routes = [
        Route(url=r'^{prefix}{trailing_slash}$',
              mapping={'get': 'list'},
              name='{basename}-list',
              initkwargs={'suffix': 'List'}),
        Route(url=r'^{prefix}/{lookup}{trailing_slash}$',
              mapping={'get': 'retrieve'},
              name='{basename}-detail',
              initkwargs={'suffix': 'Detail'})
    ]

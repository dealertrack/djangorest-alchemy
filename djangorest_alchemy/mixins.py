# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage, Page


class MultipleObjectMixin(object):
    """SQLAlchemy analog to Django's MultipleObjectMixin."""
    allow_empty = True
    query_object = None
    paginate_by = None
    paginator_class = Paginator

    def filter_query_object(self, query_object):
        """Generic filtering.

        This is a stub and has yet to be implemented.
        """
        return query_object

    def paginate_query_object(self, query_object, page_size):
        """Paginate the query object."""
        paginator = self.get_paginator(
            query_object, page_size,
            allow_empty_first_page=self.get_allow_empty())
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise InvalidPage("Page is not 'last', "
                                  "nor can it be converted to an int.")

        # DB2 fix for invalid 0 literal.
        # Generates FETCH 0 rows if not done this way
        if not paginator.count == 0:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        else:
            return (paginator, Page([], 1, paginator), [], False)

    def get_paginate_by(self, query_object):
        """Get the number of items to paginate by. None for no pagination."""
        return self.paginate_by

    def get_paginator(self, query_object, per_page, orphans=0,
                      allow_empty_first_page=True):
        """Get a paginator instance.

        The class used is overridable by setting the paginator_class
        attribute.
        """
        return self.paginator_class(
            query_object, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page)

    def get_allow_empty(self):
        """Returns True to display empty lists, False to 404."""
        return self.allow_empty

    def get_page(self, queryset):
        """Add the object list to the template context."""
        page_size = self.get_paginate_by(queryset)

        query_object = self.filter_query_object(queryset)

        paginator, page, query_object, is_paginated = \
            self.paginate_query_object(query_object, page_size)

        return query_object

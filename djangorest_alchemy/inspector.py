'''
Functions to reflect over SQLAlchemy models
'''
from sqlalchemy.orm import class_mapper


def class_keys(cls):
    """This is a utility function to get the attribute names for
    the primary keys of a class

    # >>> class_keys(Deal)
    # >>> ('dealer_code', 'deal_jacket_id', 'deal_id')
    """
    reverse_map = {}
    for name, attr in cls.__dict__.items():
        try:
            reverse_map[attr.property.columns[0].name] = name
        except:
            pass
    mapper = class_mapper(cls)
    return tuple(reverse_map[key.name] for key in mapper.primary_key)


def primary_key(cls):
    """
    Utility function to get the primary key
    of the class. In case of multiple primary keys,
    use the <classname>_id convention
    """
    has_multiple_pk = len(class_keys(cls)) > 1

    if has_multiple_pk:
        # guess the pk
        pk = cls.__name__.lower() + '_id'
    else:
        for key in class_keys(cls):
            pk = key
            break

    if not pk in cls.__dict__:
        # could not find pk field in class, now check
        # whether it has been explicitly specified
        if 'pk_field' in cls.__dict__:
            pk = cls.__dict__['pk_field']
        else:
            raise Exception("Could not figure out primary key field"
                            " for %s model. Tried to first use %s as field name, and then"
                            "looked for pk_field attr which was also missing" % (cls.__name__, pk))

    return pk



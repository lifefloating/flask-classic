import re
import logging
from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from pylc3.exceptions import NotFoundException

log = logging.getLogger(__name__)


class ModelBase(object):
    """Base class for models."""

    id = Column(
        INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )

    @declared_attr
    def __tablename__(cls):

        if cls.__name__ == 'TestTable01':
            name = 'test_table01'
        # elif cls.__name__ == 'XXXX':
        #     name = 'xxx'
        return name

    def __init__(self, dict_data=None):
        """Init instance from dict_data

        :param dict_data: json data to parse
        :type dict_data: dict
        """
        if dict_data is not None:
            for key, value in dict_data.items():
                real_key = key.lower()

                # validate json data
                if isinstance(value, list):
                    continue
                try:
                    getattr(self, real_key)
                except Exception as e:
                    log.error(
                        "Invalid attribute %s in %s: %s" % (key, dict_data, e)
                    )
                    continue

                setattr(self, real_key, value)

    def to_dict(self, property_list=None):
        properties = {
            c.name.upper(): getattr(self, c.name, None)
            for c in self.__table__.columns
        }
        if property_list:
            for p in property_list:
                properties[p.upper()] = getattr(self, p, None)
        return properties

    def update(self, dict_info):
        for k, v in dict_info.items():
            setattr(self, k, v)
        return

    @classmethod
    def apply_filters(cls, query, filters):
        """Apply filters to a query.

        :param query: The query to apply filters to.
        :param filters: The filters to apply.
        :type filters: dict or sqlalchemy filter

        :returns: The query with filters applied to it.
        """
        if isinstance(filters, dict):
            if filters:
                for k, v in filters.items():
                    column = getattr(cls, k, None)
                    if column is None:
                        continue
                    else:
                        query = query.filter(column == v)
        elif filters is not None:
            query = query.filter(filters)
        return query

    @classmethod
    def get_one(cls, session, filters=None):
        """Get a specific object. If result is None or more than one,
            return exception.

        :param session: sqlalchemy session
        :param filters: The filters to apply.
        :type filters: dict or sqlalchemy filter

        :returns: The object for said model with filters applied.
        """
        return cls.apply_filters(session.query(cls), filters).one()

    @classmethod
    def get_first(cls, session, filters=None):
        """Get a specific object.

        :param session: sqlalchemy session
        :param filters: The filters to apply.
        :type filters: dict or sqlalchemy filter

        :returns: The object for said model with filters applied.
        """
        return cls.apply_filters(session.query(cls), filters).first()

    @classmethod
    def get_collection(cls, session, filters=None):
        """Get a specific collection.

        :param session: sqlalchemy session
        :param filters: The filters to apply.
        :type filters: dict or sqlalchemy filter

        :returns: The objects for said model with filters applied.
        """
        return cls.apply_filters(session.query(cls), filters).all()

    @classmethod
    def get_by_id(cls, session, obj_id, field=None):
        """Query the model with the given context for a specific object.

        :param session: sqlalchemy session
        :param obj_id: The ID of the object to query for.
        :param field: specific field, string or list of string
        :returns: The object with the give obj_id for the model,
                  raise DeepFlow NotFoundException if result is None.
        """
        try:
            if field is None:
                obj = cls.get_one(session, {'id': obj_id})
            else:
                if isinstance(field, list):
                    columns = [getattr(cls, f) for f in field]
                    return cls.apply_filters(
                        session.query(*columns), {
                            'id': obj_id
                        }
                    ).one()
                else:
                    return cls.apply_filters(
                        session.query(getattr(cls, field)), {
                            'id': obj_id
                        }
                    ).one()
        except (NoResultFound, MultipleResultsFound):
            raise NotFoundException(
                resource=cls.__name__, option='id', value=obj_id
            )
        return obj

    @classmethod
    def get_by_lcuuid(cls, session, lcuuid, field=None):
        """Query the model with the given context for a specific object.

        :param session: sqlalchemy session
        :param lcuuid: The ID of the object to query for.
        :param field: specific field, string or list of string
        :returns: The object with the give lcuuid for the model,
                  raise DeepFlow NotFoundException if result is None.
        """
        try:
            if field is None:
                obj = cls.get_one(session, {'lcuuid': lcuuid})
            else:
                if isinstance(field, list):
                    columns = [getattr(cls, f) for f in field]
                    return cls.apply_filters(
                        session.query(*columns), {
                            'lcuuid': lcuuid
                        }
                    ).one()
                else:
                    return cls.apply_filters(
                        session.query(getattr(cls, field)), {
                            'lcuuid': lcuuid
                        }
                    ).one()
        except (NoResultFound, MultipleResultsFound):
            raise NotFoundException(
                resource=cls.__name__, option='lcuuid', value=lcuuid
            )
        return obj

    @classmethod
    def get_field_collection(cls, session, field, filters=None):
        """Get a specific field collection.

        :param session: sqlalchemy session
        :param field: a specific field
        :param filters: The filters to apply.
        :type filters: dict or sqlalchemy filter

        :returns: The objects for said model with filters applied.
        """
        if isinstance(field, list):
            columns = [getattr(cls, f) for f in field]
            return cls.apply_filters(session.query(*columns), filters).all()
        else:
            return cls.apply_filters(
                session.query(getattr(cls, field)), filters
            ).all()

    @classmethod
    def delete_by_filters(cls, session, filters=None):
        cls.apply_filters(session.query(cls), filters).\
            delete(synchronize_session='fetch')
        session.commit()
        return

    @classmethod
    def delete_by_lcuuid(cls, session, lcuuid):
        return cls.delete_by_filters(session, {'lcuuid': lcuuid})

    @classmethod
    def get_collection_count(cls, session, filters=None):
        """Get the count for a specific collection.

        :param session: sqlalchemy session
        :param filters: The filters to apply.
        :type filters: dict or sqlalchemy filter

        :returns: The number of objects for the model with filters applied.
        """
        return cls.apply_filters(session.query(func.count(cls.id)),
                                 filters).scalar()

    @classmethod
    def get_one_without_deleted(cls, session, filters=None):
        """Get a specific object not deleted. If result is None or more than one,
            return NotFoundException.

        :param session: sqlalchemy session
        :param filters: The filters to apply.
        :type filters: dict or sqlalchemy filter

        :returns: The object for said model with filters applied.
        """
        query = cls.apply_filters(session.query(cls), filters)
        try:
            return query.filter(cls.deleted.is_(False)).one()
        except (NoResultFound, MultipleResultsFound):
            raise NotFoundException(resource=cls.__name__)


MysqlBase = declarative_base(cls=ModelBase, constructor=None)

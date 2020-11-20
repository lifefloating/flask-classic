import logging
from flask import g
from models import  TestDomain
from sqlalchemy import text

log = logging.getLogger(__name__)

'''
    @example by testDomain
'''
# from db_base import db_session


class FlaskDaoTestDb(object):

    testdomain = TestDomain

    # @classmethod
    # def get_current(cls):
    #     return g.current

    @classmethod
    def get_list(cls, _where=None, _query=None):
        db = g.session
        where_info = ""
        if _where is not None:
            where_info = _where
        if _query is not None:
            res = db.query(*_query)
        else:
            res = db.query(cls.testdomain)

        # if _del:
        #     res = res.filter_by(deleted=0)

        return res.filter(text(where_info)).order_by(
            cls.testdomain.id.desc()).all()

    @classmethod
    def get_detail(cls, _where=None, _query=None):
        where_info = ""
        db = g.session
        if _where is not None:
            where_info = _where

        if _query is not None:
            res = db.query(*_query)
        else:
            res = db.query(cls.testdomain)

        result = res.filter(text(where_info)).order_by(
            cls.testdomain.id.desc()).first()
        if result:
            if _query is not None:
                ret = result
            else:
                ret = result.to_dict()
            return ret
        else:
            return None

    @classmethod
    def count(cls, where=None):
        db = g.session
        where_info = ""
        if where is not None:
            where_info = where
        return db.query(cls.testdomain.id).filter(text(where_info)).count()

    @classmethod
    def update(cls, domain, id):
        db = g.session
        db.query(cls.testdomain).filter_by(id=id).update(domain)
        db.commit()

        res = db.query(cls.testdomain).get(id)
        if res:
            return res.to_dict()
        else:
            return None

    @classmethod
    def add(cls, domain):
        db = g.session
        domain_info = cls.testdomain(domain)
        db.add(domain_info)
        db.commit()
        return domain_info

    @classmethod
    def delete(cls, id):
        db = g.session
        filter_list = []
        if id:
            db.query(cls.testdomain).filter_by(id=id).delete()

        return db.commit()


flask_dao_test_db = FlaskDaoTestDb()

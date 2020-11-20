# coding: utf-8
from sqlalchemy import (
    BigInteger, Column, DateTime, Index, Integer, Numeric, SmallInteger,
    String, Text, text
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata



class TestDomain(Base):
    __tablename__ = 'test_domain'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    dis_name = Column(String(64), server_default=text("''"))
    ip = Column(String(64))
    role = Column(Integer, server_default=text("'0'"))
    ip2 = Column(String(50))

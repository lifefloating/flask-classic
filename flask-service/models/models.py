import datetime
from sqlalchemy import String, Column, ForeignKey, text, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import (
    TIMESTAMP, INTEGER, CHAR, DATETIME, VARCHAR, TEXT, BIGINT, TINYINT,
    LONGTEXT
)

from .base import MysqlBase


class TestDomain(MysqlBase):
    
    name = Column(VARCHAR(length=64))
    dis_name = Column(VARCHAR(length=64))
    ip = Column('ip', CHAR(length=64))
    role = Column('role', INTEGER())
    type = Column('type', INTEGER())
    ip2 = Column('ip2', CHAR(length=64))

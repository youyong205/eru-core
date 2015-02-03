#!/usr/bin/python
#coding:utf-8

from eru.models import db
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

class DBBase(db.Model):

    __abstract__ = True

    @declared_attr
    def id(cls):
        return db.Column('id', db.Integer, primary_key=True)

    @declared_attr
    def aid(cls):
        return db.Column(db.Integer, db.ForeignKey('apps.id'))

    @declared_attr
    def username(cls):
        return db.Column(db.CHAR(16), nullable=False)

    @declared_attr
    def password(cls):
        return db.Column(db.CHAR(32), nullable=False)

    @declared_attr
    def database(cls):
        return db.Column(db.CHAR(32), nullable=False)

    @declared_attr
    def address(cls):
        return db.Column(db.String(255), nullable=False)

    @declared_attr
    def created(cls):
        return db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, database, address):
        self.username = username
        self.password = password
        self.database = database
        self.address = address

class MySQL(DBBase):
    __tablename__ = 'mysql'

class InfluxDB(DBBase):
    __tablename__ = 'influxdb'

#TODO redis/etcd


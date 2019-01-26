
from sqlalchemy import (
    Column,
    Integer,
    Text,
    func,
    String,
    Boolean,
    DateTime,
    Date,
    TIMESTAMP,
    ForeignKey,
    or_,
    and_,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import expression
from sqlalchemy.ext.declarative import AbstractConcreteBase
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class List(db.Model):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)
    items = relationship("ListItem", back_populates="llist")


class Company(db.Model):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)
    tracked = Column(Boolean, server_default=expression.true(), nullable=False)


class Geo(db.Model):
    __tablename__ = "geos"

    id = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)


from sqlalchemy.ext.declarative import declared_attr


class ListItem(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    @declared_attr
    def list_id(cls):
        return Column(ForeignKey("lists.id"), nullable=False)

    @declared_attr
    def llist(cls):
        return relationship("List", back_populates="List")


class CompanyListItem(ListItem):
    __tablename__ = "company_list_item"

    company_id = Column(ForeignKey("companies.id", deferrable=True, initially="DEFERRED"), nullable=False)
    company = relationship("Company", primaryjoin="CompanyListItem.company_id == Company.id")

    __mapper_args__ = {"polymorphic_identity": "company_item", "concrete": True}


class GeoListItem(ListItem):
    __tablename__ = "geo_list_item"

    geo_id = Column(ForeignKey("geos.id"), nullable=False)
    geo = relationship("Geo")

    __mapper_args__ = {"polymorphic_identity": "geo_item", "concrete": True}

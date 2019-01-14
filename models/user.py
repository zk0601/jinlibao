from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, DATETIME, ForeignKey
from datetime import datetime

Base = declarative_base()


#user_base_model
class User_Base(Base):
    __tablename__ = 'user_base'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    openid = Column(VARCHAR(255), unique=True)
    nickname = Column(VARCHAR(255), nullable=False)
    image_url = Column(VARCHAR(255), nullable=False)
    gender = Column(VARCHAR(12))
    province = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    country = Column(VARCHAR(255))
    create_time = Column(DATETIME, default=datetime.now(), nullable=False)

    def keys(self):
        return [c.name for c in self.__table__.columns]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


#user_form_model
class User_From(Base):
    __tablename__ = 'user_form'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    openid = Column(VARCHAR(255), unique=True)
    gender = Column(VARCHAR(12), nullable=False)
    family = Column(INTEGER, nullable=False)
    children_num = Column(INTEGER, ForeignKey("spouse.id"), nullable=False, default=0)
    spouse_id = Column(INTEGER, ForeignKey("children.id"), default=None)
    first_child_id = Column(INTEGER, ForeignKey("children.id"), default=None)
    second_child_id = Column(INTEGER, ForeignKey("children.id"), default=None)
    third_child_id = Column(INTEGER, ForeignKey("children.id"), default=None)
    is_supportparents = Column(INTEGER, nullable=False)
    birthday = Column(VARCHAR(255), nullable=False)
    is_sick = Column(INTEGER, nullable=False)
    disease = Column(VARCHAR(255), default="")
    income = Column(INTEGER, nullable=False)
    profession = Column(VARCHAR(255), nullable=False)
    has_socialsecurity = Column(INTEGER, nullable=False)
    has_housloans = Column(INTEGER, nullable=False)
    houseloans_total = Column(INTEGER, default=None)
    houseloans_permonth = Column(INTEGER, default=None)
    houseloans_years = Column(INTEGER, default=None)
    has_carloans = Column(INTEGER, nullable=False)
    carloans_total = Column(INTEGER, default=None)
    carloans_permonth = Column(INTEGER, default=None)
    carloans_years = Column(INTEGER, default=None)
    offen_businesstravel = Column(INTEGER, nullable=False)
    offen_car = Column(INTEGER, nullable=False)
    city = Column(VARCHAR(255), nullable=False)
    create_time = Column(DATETIME, default=datetime.now(), nullable=False)

    def keys(self):
        return [c.name for c in self.__table__.columns]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Spouse(Base):
    __tablename__ = 'spouse'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    birthday = Column(VARCHAR(255), nullable=False)
    is_sick = Column(INTEGER, nullable=False)
    disease = Column(VARCHAR(255), default="")
    income = Column(INTEGER, nullable=False)
    profession = Column(VARCHAR(255), nullable=False)
    has_socialsecurity = Column(INTEGER, nullable=False)
    offen_businesstravel = Column(INTEGER, nullable=False)
    offen_car = Column(INTEGER, nullable=False)

    def keys(self):
        return [c.name for c in self.__table__.columns]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Children(Base):
    __tablename__ = 'children'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    gender = Column(VARCHAR(12), nullable=False)
    birthday = Column(VARCHAR(255), nullable=False)
    is_sick = Column(INTEGER, nullable=False)
    disease = Column(VARCHAR(255), default="")

    def keys(self):
        return [c.name for c in self.__table__.columns]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Phone_Name(Base):
    __tablename__ = 'phone_name'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    openid = Column(VARCHAR(255), unique=True)
    name = Column(VARCHAR(255), nullable=False)
    phone = Column(VARCHAR(255), nullable=False)
    wx_number = Column(VARCHAR(255), nullable=False)

    def keys(self):
        return [c.name for c in self.__table__.columns]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

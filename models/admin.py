from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, DATETIME, DECIMAL, ForeignKey

Base = declarative_base()


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)

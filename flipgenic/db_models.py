from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    ngt_id = Column(Integer)
    response = Column(String)

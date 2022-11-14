from sqlalchemy import engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


SQLBase = declarative_base()


class Shortener(SQLBase):
    __tablename__ = "shortener"

    id = Column(Integer, primary_key=True)

    url = Column(String(1024), index=True)
    shortened = Column(String(20), index=True)
    token = Column(String(30))
    visits = Column(Integer)
    expire_time = Column(DateTime, index=True)

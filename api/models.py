from sqlalchemy import Column, Integer, String
from database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    link = Column(String, unique=True)
    date = Column(String)
    labels = Column(String)
    content = Column(String)
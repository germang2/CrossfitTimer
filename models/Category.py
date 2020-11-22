from engine import db

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Category(db.Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    persons = relationship('Athlete', backref='people')

    def __repr__(self) -> str:
        return f'Category({self.name})'

    def __str__(self) -> str:
        return self.name
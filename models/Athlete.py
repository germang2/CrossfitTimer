from sqlalchemy.orm import backref
from engine import db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Athlete(db.Base):
    __tablename__ = 'athletes'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(40), nullable=False)
    club = Column(String(20), nullable=True)
    nit = Column(String(20), unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('models.Category.Category', backref='athletes')
    dorsal = Column(String(10), nullable=True, unique=True)

    def __init__(self, full_name, club, category_id, nit, dorsal):
        self.full_name = full_name
        self.club = club
        self.category_id = category_id
        self.nit = nit
        self.dorsal = dorsal

    def __repr__(self):
        return f'Athlete({self.full_name}'

    def __str__(self):
        return f'{self.full_name}'
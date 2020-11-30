from sqlalchemy.orm import backref
from engine import db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Athlete(db.Base):
    __tablename__ = 'athletes'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    age = Column(Integer, nullable=False)
    club = Column(String(20), nullable=True)
    nit = Column(String(20), unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    #competences = relationship('CompetenceAthlete', backref='competences')

    def __init__(self, name, last_name, age, club, category_id, nit):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.club = club
        self.category_id = category_id
        self.nit = nit

    def __repr__(self):
        return f'Athlete({self.name}, {self.last_name}, {self.age})'

    def __str__(self):
        return f'{self.name} {self.last_name}'
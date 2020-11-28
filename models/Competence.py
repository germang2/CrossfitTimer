from engine import db

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship


class Competence(db.Base):
    __tablename__ = 'competences'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    place = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(String(15), nullable=False)
    reward = Column(String(100), nullable=True)
    #athletes = relationship('CompetenceAthlete', backref='athletes')
    #groups = relationship('Group', backref='groups')

    def __init__(self, name, place, date, time, reward=None, details=None):
        self.name = name
        self.place = place
        self.date = date
        self.time = time
        self.reward = reward
        self.details = details

    def __repr__(self) -> str:
        return f'Competence({self.name}, {self.place}, {self.time})'

    def __str__(self) -> str:
        return f'{self.name} -> {self.place} -> {self.date}'
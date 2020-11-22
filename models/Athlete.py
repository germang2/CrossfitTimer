from engine import db

from sqlalchemy import Column, Integer, String, Float

class Athlete(db.Base):
    __tablename__ = 'Athlete'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def __init__(self, name, last_name, age):
        self.name = name
        self.last_name = last_name
        self.age = age

    def __repr__(self):
        return f'Athlete({self.name}, {self.last_name}, {self.age})'

    def __str__(self):
        return f'{self.name} {self.last_name}'
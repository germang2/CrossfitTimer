from ast import Str
from engine import db
from models.Athlete import Athlete
from models.Group import Group
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship


class GroupAthlete(db.Base):
    __tablename__ = 'groups_athletes'

    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer, ForeignKey('athletes.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    dorsal = Column(String(10), nullable=True)
    initial_time = Column(DateTime, nullable=True)
    final_time = Column(DateTime, nullable=True)
    total_time = Column(DateTime, nullable=True)
    observations = Column(Text, nullable=True)
    athlete = relationship(Athlete, backref='athletes')
    group = relationship(Group, backref='groups')

    def __str__(self):
        return f'{self.athlete}, {self.dorsal}'

    def __repr__(self):
        return f'{self.athlete} -> {self.group} -> {self.dorsal}'

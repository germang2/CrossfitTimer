from ast import Str
from engine import db

from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey

class CompetenceAthlete(db.Base):
    __tablename__ = 'competences_athletes'

    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer, ForeignKey('athletes.id'))
    competence_id = Column(Integer, ForeignKey('competences.id'))
    dorsal = Column(String(10), nullable=False)
    initial_time = Column(Time, nullable=False)
    final_time = Column(Time, nullable=False)
    total_time = Column(Time, nullable=False)
    observations = Column(Text, nullable=True)



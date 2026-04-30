from ast import Str
from engine import db
from models.Athlete import Athlete
from models.Group import Group
from sqlalchemy import Column, Integer, String, DateTime, Time, Text, ForeignKey, Boolean, func, cast
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import timedelta


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
    tasks_completed = Column(String(10), nullable=True)
    penalty = Column(Time, nullable=True)
    status = Column(Boolean, default=True)

    @hybrid_property
    def adjusted_total_time(self):
        if self.total_time and self.penalty:
            penalty_delta = timedelta(
                hours=self.penalty.hour,
                minutes=self.penalty.minute,
                seconds=self.penalty.second,
                microseconds=self.penalty.microsecond
            )
            return self.total_time + penalty_delta
        return self.total_time

    @adjusted_total_time.expression
    def adjusted_total_time(cls):
        penalty_str = cast(func.coalesce(cls.penalty, '00:00:00'), String)
        return func.datetime(
            cls.total_time, 
            '+' + func.substr(penalty_str, 1, 2) + ' hours',
            '+' + func.substr(penalty_str, 4, 2) + ' minutes',
            '+' + func.substr(penalty_str, 7, 2) + ' seconds'
        )

    def __str__(self):
        return f'{self.athlete}, {self.dorsal}'

    def __repr__(self):
        return f'{self.athlete} -> {self.group} -> {self.dorsal}'

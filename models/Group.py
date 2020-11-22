from engine import db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Group(db.Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    competence_id = Column(Integer, ForeignKey('competences.id'), nullable=False)
    order = Column(Integer, default=1)

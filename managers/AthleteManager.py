from engine import db
from models.Athlete import Athlete


class AthleteManager:

    @staticmethod
    def get_athletes_by_filters(filters, order='full_name'):
        return db.session.query(Athlete).filter(*filters).order_by(order).all()

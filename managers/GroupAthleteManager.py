from engine import db
from models.GroupAthlete import GroupAthlete
from models.Group import Group
from models.Competence import Competence
from models.Athlete import Athlete
from models.GroupAthlete import GroupAthlete


class GroupAthleteManager:

    @staticmethod
    def get_group_athletes_by_filters(filters, join_group=False, order='dorsal'):
        try:
            query = db.session.query(GroupAthlete)
            if join_group:
                query = query.join(Group, Group.id == GroupAthlete.group_id)
            query = query.filter(*filters).order_by(order)
            return query.all()
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def filter_athletes_by_dorsal(filters):
        try:
            query = db.session.query(GroupAthlete)\
                .join(Athlete, Athlete.id == GroupAthlete.athlete_id)\
                .join(Group, Group.id == GroupAthlete.group_id)\
                .join(Competence, Competence.id == Group.competence_id)
            query = query.filter(*filters)
            return query.order_by(GroupAthlete.dorsal).all()

        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_athlete_by_dorsal(dorsal, competence_id):
        try:
            query = (
                db.session.query(GroupAthlete)
                .join(Group, Group.id == GroupAthlete.group_id)
            )
            query = query.filter(GroupAthlete.dorsal == dorsal, Group.competence_id == competence_id)
            group_athlete = query.first()
            if group_athlete:
                query = (
                    db.session.query(Athlete)
                    .filter(Athlete.id == group_athlete.athlete_id)
                )
                athlete = query.first()
                return athlete, group_athlete
            return None, None
        except Exception as e:
            print(e)
            return {}

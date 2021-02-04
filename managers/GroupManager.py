from engine import db
from models.Group import Group


class GroupManager:

    @staticmethod
    def get_groups_by_filters(filters, order='order'):
        try:
            return db.session.query(Group).filter(*filters).order_by(order)
        except Exception as e:
            print(e)
            return []

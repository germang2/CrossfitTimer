from faker import Faker

from engine import db
from models.Competence import Competence
from models.Group import Group


fake = Faker()

competence_name = "Energia extrema"


def get_group_data(competence, index):
    return {
        "name": f"{competence.name} - {index}",
        "competence_id": f"{competence.id}",
        "order": index,
    }


if __name__ == '__main__':
    session = db.session
    competence = session.query(Competence).filter_by(name=competence_name).first()
    if competence:
        group_list = []
        for i in range(1, 21):
            group_data = get_group_data(competence, i)
            group_obj = Group(**group_data)
            group_list.append(group_obj)
        print(f"adding {len(group_list)} groups to database")
        session.bulk_save_objects(group_list)
        session.commit()
        print("Done!!")
    else:
        print(f"Category {category_name} not found. Skipping process")
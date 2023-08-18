from faker import Faker

from engine import db
from models.Athlete import Athlete
from models.Category import Category


fake = Faker()

category_name = "haka"
club_name = "Haka"


def get_athlete_data(category, dorsal):

    return {
        "full_name": fake.name(),
        "club": club_name,
        "category_id": category.id,
        "nit": fake.random_int(1000, 1000000),
        "dorsal": dorsal,
    }


def create_athlete(full_name, club, category_id, nit, dorsal):
    athlete = Athlete(
        full_name=full_name,
        club=club,
        category_id=category_id,
        nit=nit,
        dorsal=dorsal
    )


if __name__ == '__main__':
    session = db.session
    category = session.query(Category).filter_by(name=category_name).first()
    if category:
        athletes_list = []
        for i in range(100, 1000):
            athlete_data = get_athlete_data(category, dorsal=i)
            athlete_obj = Athlete(**athlete_data)
            athletes_list.append(athlete_obj)
        print(f"adding {len(athletes_list)} athletes to database")
        session.bulk_save_objects(athletes_list)
        session.commit()
        print("Done!!")
    else:
        print(f"Category {category_name} not found. Skipping process")

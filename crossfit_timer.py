from engine import db
from models.Category import Category
from models.Athlete import Athlete
from models.Competence import Competence
from models.CompetenceAthlete import CompetenceAthlete
from models.Group import Group

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    

    

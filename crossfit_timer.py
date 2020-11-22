from engine import db
from models.Athlete import Athlete

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    

    

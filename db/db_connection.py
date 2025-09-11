import sqlalchemy as db
import sqlalchemy.orm as dbo
import os
from dotenv import load_dotenv

load_dotenv()

engine = db.create_engine(os.getenv("db_url"))
Session = dbo.sessionmaker(bind=engine)
Base = dbo.declarative_base()




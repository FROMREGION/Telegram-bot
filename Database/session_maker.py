from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Database import DatabaseGetter


database_getter = DatabaseGetter()


def make_session():
    engine = create_engine(f'sqlite:///{database_getter()}', echo=False)
    return sessionmaker(bind=engine)()

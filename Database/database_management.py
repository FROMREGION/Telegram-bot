from sqlalchemy import create_engine, MetaData, Table
from Database import DatabaseGetter, make_session, USER_TABLE_NAME, User, EVENT_TABLE_NAME, Event
from JsonGetter import JSON
from os import remove


DATABASE_NAME = 'users_and_events.db'
json_getter = JSON()
database_getter = DatabaseGetter()
_, SUPERUSER_ID, *_ = json_getter()


def check_database():
    database_name = database_getter(without_exceptions=True)
    if database_name:
        if database_name == DATABASE_NAME:
            session = make_session()
            try:
                superuser = session.query(User).filter_by(user_id=SUPERUSER_ID).first()
                if superuser is None:
                    session.add(User(SUPERUSER_ID, True, False, False, 0))
                else:
                    superuser.is_admin, superuser.is_pdt, superuser.is_promotion = True, False, False
                    superuser.subscription = 0
                session.commit()
                session.close()
                print('Database was checked!')
            except Exception:
                session.close()
                remove(database_name)
                __make_database()
                print('Database was recreated and filled!')
        else:
            remove(database_name)
            __make_database()
            print('Database was created and filled!')
    else:
        __make_database()
        print('Database was created and filled!')


def __make_database():
    engine = create_engine(f'sqlite:///{DATABASE_NAME}', echo=False)
    metadata = MetaData()
    users_table = Table(USER_TABLE_NAME, metadata, *User.get_all_columns_with_attributes())
    events_table = Table(EVENT_TABLE_NAME, metadata, *Event.get_all_columns_with_attributes())
    metadata.create_all(engine)
    __fill_database()


def __fill_database():
    session = make_session()
    session.add(User(SUPERUSER_ID, True, False, False, 0))
    session.commit()
    session.close()

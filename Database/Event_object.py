from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Boolean, Column, String
from Database import make_session


EVENT_TABLE_NAME = 'events'
Base = declarative_base()


class Event(Base):
    __tablename__ = EVENT_TABLE_NAME
    time = Column(Integer, primary_key=True)
    day = Column(String, primary_key=True)
    chat_id = Column(Integer)
    message_id = Column(Integer)
    for_admins = Column(Boolean)
    for_pdts = Column(Boolean)
    for_promotions = Column(Boolean)

    def __init__(self, time, day, chat_id, message_id, for_admins, for_pdts, for_promotions):
        self.time = time
        self.day = day
        self.chat_id = chat_id
        self.message_id = message_id
        self.for_admins = for_admins
        self.for_pdts = for_pdts
        self.for_promotions = for_promotions

    def __repr__(self):
        return f"<Database.Event("\
               f"time={self.time}, "\
               f"day='{self.day}', "\
               f"chat_id={self.chat_id}, "\
               f"message_id={self.message_id}, "\
               f"for_admins={self.for_admins}, "\
               f"for_pdts={self.for_pdts}, "\
               f"for_promotions={self.for_promotions}"\
               f")>"

    @staticmethod
    def get_all_columns_with_attributes():
        return Column('time', Integer, primary_key=True),\
               Column('day', String, primary_key=True),\
               Column('chat_id', Integer),\
               Column('message_id', Integer),\
               Column('for_admins', Boolean),\
               Column('for_pdts', Boolean),\
               Column('for_promotions', Boolean)


def update_event(time, day, chat_id, message_id, for_admins, for_pdts, for_promotions):
    session = make_session()
    event = session.query(Event).filter_by(time=time, day=day).first()
    if event is None:
        session.add(Event(time, day, chat_id, message_id, for_admins, for_pdts, for_promotions))
    else:
        event.chat_id, event.message_id = chat_id, message_id
        event.for_admins, event.for_pdts, event.for_promotions = for_admins, for_pdts, for_promotions
    session.commit()
    session.close()


def del_event(time, day):
    session = make_session()
    event = session.query(Event).filter_by(time=time, day=day).first()
    if event is not None:
        session.delete(event)
        session.commit()
    session.close()


def del_all_events():
    session = make_session()
    events = session.query(Event).all()
    for event in events:
        session.delete(event)
    session.commit()
    session.close()


def del_events_for_a_day(day):
    session = make_session()
    events = session.query(Event).filter_by(day=day).all()
    for event in events:
        session.delete(event)
    session.commit()
    session.close()


def del_admin_events():
    session = make_session()
    events = session.query(Event).filter_by(for_admins=True).all()
    for event in events:
        session.delete(event)
    session.commit()
    session.close()


def del_pdt_events():
    session = make_session()
    events = session.query(Event).filter_by(for_pdts=True).all()
    for event in events:
        session.delete(event)
    session.commit()
    session.close()


def del_promotion_events():
    session = make_session()
    events = session.query(Event).filter_by(for_promotions=True).all()
    for event in events:
        session.delete(event)
    session.commit()
    session.close()


def get_event(time, day):
    session = make_session()
    event = session.query(Event).filter_by(time=time, day=day).first()
    session.close()
    return event


def get_all_events():
    session = make_session()
    events = session.query(Event).all()
    session.close()
    return events


def get_admin_events():
    session = make_session()
    admin_events = session.query(Event).filter_by(for_admins=True).all()
    session.close()
    return admin_events


def get_pdt_events():
    session = make_session()
    pdt_events = session.query(Event).filter_by(for_pdts=True).all()
    session.close()
    return pdt_events


def get_promotion_events():
    session = make_session()
    promotion_events = session.query(Event).filter_by(for_promotions=True).all()
    session.close()
    return promotion_events

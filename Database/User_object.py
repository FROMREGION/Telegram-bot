from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Boolean, Column
from Database import make_session


USER_TABLE_NAME = 'users'
Base = declarative_base()


class User(Base):
    __tablename__ = USER_TABLE_NAME
    user_id = Column(Integer, primary_key=True)
    is_admin = Column(Boolean)
    is_pdt = Column(Boolean)
    is_promotion = Column(Boolean)
    subscription = Column(Integer)

    def __init__(self, user_id, is_admin, is_pdt, is_promotion, subscription):
        self.user_id = user_id
        self.is_admin = is_admin
        self.is_pdt = is_pdt
        self.is_promotion = is_promotion
        self.subscription = subscription

    def __repr__(self):
        return f"<Database.User("\
               f"user_id={self.user_id}, "\
               f"is_admin={self.is_admin}, "\
               f"is_pdt={self.is_pdt}, "\
               f"is_promotion={self.is_promotion}"\
               f"subscription={self.subscription}"\
               f")>"

    @staticmethod
    def get_all_columns_with_attributes():
        return Column('user_id', Integer, primary_key=True),\
               Column('is_admin', Boolean),\
               Column('is_pdt', Boolean),\
               Column('is_promotion', Boolean),\
               Column('subscription', Integer)


def update_user(user_id, is_admin, is_pdt, is_promotion, subscription):
    session = make_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if user is None:
        session.add(User(user_id, is_admin, is_pdt, is_promotion, subscription))
    else:
        user.is_admin, user.is_pdt, user.is_promotion = is_admin, is_pdt, is_promotion
        user.subscription = subscription
    session.commit()
    session.close()


def del_user(user_id):
    session = make_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if user is not None:
        session.delete(user)
        session.commit()
    session.close()


def get_user(user_id):
    session = make_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    session.close()
    return user


def get_all_users():
    session = make_session()
    users = session.query(User).all()
    session.close()
    return users


def get_admin_users():
    session = make_session()
    admins = session.query(User).filter_by(is_admin=True).all()
    session.close()
    return admins


def get_pdt_users():
    session = make_session()
    pdts = session.query(User).filter_by(is_pdt=True).all()
    session.close()
    return pdts


def get_promotion_users():
    session = make_session()
    promotions = session.query(User).filter_by(is_promotion=True).all()
    session.close()
    return promotions


def update_subscription_days():
    session = make_session()
    promotions = session.query(User).filter_by(is_promotion=True).all()
    for promotion in promotions:
        if promotion.subscription <= 1:
            promotion.is_promotion = False
            promotion.subscription = 0
        else:
            promotion.subscription -= 1
    session.commit()
    session.close()

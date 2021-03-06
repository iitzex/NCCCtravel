from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(String(20))
    address = Column(String(50))
    city = Column(String(20))
    town = Column(String(20))
    main = Column(String(20))
    sub = Column(String(20))
    lat = Column(Float(20))
    lon = Column(Float(20))

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.phone, self.address)


def init():
    engine = create_engine('sqlite:///nccc.db', echo=True)
    Base.metadata.create_all(engine)
    print(engine)


def test():
    engine = create_engine('sqlite:///nccc.db', echo=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    al = session.query(Store).all()
    print(al)
    # a = Store(name='aa', phone='0x', address='')
    # b = Store(name='bb', phone='0x', address='')
    # session.add(a)
    # session.add(b)
    # session.commit()
    print('+++')
    for i in session.query(Store).order_by(Store.name):
        print(i)
        # session.delete(i)
    session.commit()

if __name__ == '__main__':
    init()


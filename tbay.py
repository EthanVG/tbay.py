#Users should be able to auction multiple items: One(User) to Many(Items)
#Users should be able to bid on multiple items: One(User) to Many(Bids)
#Multiple users should be able to place a bid on an item: Many(User) to One(Item:Bid)
#session.query(User).all()[0].items[0].name: returns the name of item [0]

#To get highest bid.
#highest_bid = session.query(Bid).order_by(Bid.price).all().pop()
#print(highest_bid.user.username, highest_bid.price)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime

from sqlalchemy import Table, Column, Integer, Float, String, DateTime, ForeignKey

class Item(Base):
    __tablename__ = "item"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    bids = relationship("Bid", backref="item")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
        
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    items = relationship("Item", backref="user")
    bids = relationship("Bid", backref="user")
    
class Bid(Base):
    __tablename__ = "bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    
Base.metadata.create_all(engine)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///database/app.db')
Session = sessionmaker(bind=engine)
session = Session()

class Mission(Base):
    __tablename__ = 'missions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)

Base.metadata.create_all(engine)

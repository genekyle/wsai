from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# Define the base class for ORM
Base = declarative_base()

# Define ORM classes for your tables
class UserProfile(Base):
    __tablename__ = 'UserProfiles'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    searches = relationship("Search", back_populates="user_profile")

class Search(Base):
    __tablename__ = 'Searches'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('UserProfiles.id'))
    job_title = Column(String)
    location = Column(String)
    radius = Column(String)
    timestamp = Column(DateTime)
    user_profile = relationship("UserProfile", back_populates="searches")
    jobs = relationship("Job", back_populates="search")

class Job(Base):
    __tablename__ = 'Jobs'
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey('Searches.id'))
    job_title = Column(String)
    company_name = Column(String)
    location = Column(String)
    date_scraped = Column(String)
    date_recorded = Column(DateTime)
    skills = Column(String)
    education = Column(String)
    job_description = Column(String)
    search = relationship("Search", back_populates="jobs")

# Set the path of the SQLite database
DATABASE_PATH = os.path.join("db", "indeed_db.db")

# Create the SQLAlchemy engine to connect to the SQLite database
engine = create_engine(f'sqlite:///{DATABASE_PATH}')

# Create a sessionmaker, bound to the engine
Session = sessionmaker(bind=engine)

# Method to initialize the database
def init_db():
    print('initializing Indeed DB')
    Base.metadata.create_all(engine)
    print('Indeed Database Initialized')

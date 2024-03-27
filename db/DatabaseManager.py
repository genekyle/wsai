from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
import os

# Define separate base classes for Indeed and LinkedIn
IndeedBase = declarative_base()
LinkedInBase = declarative_base()

# Define ORM classes for your Indeed tables
class IndeedUserProfile(IndeedBase):
    __tablename__ = 'indeed_user_profiles'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    searches = relationship("IndeedSearch", back_populates="user_profile")

class IndeedSearch(IndeedBase):
    __tablename__ = 'indeed_searches'
    id = Column(Integer, primary_key=True)      
    user_profile_id = Column(Integer, ForeignKey('indeed_user_profiles.id'))
    search_entry = Column(String)
    location = Column(String)
    radius = Column(String)
    timestamp = Column(DateTime)
    total_scraped = Column(Integer)
    search_amount = Column(Integer)
    user_profile = relationship("IndeedUserProfile", back_populates="searches")
    jobs = relationship("IndeedJob", back_populates="search")

class IndeedJob(IndeedBase):
    __tablename__ = 'indeed_jobs'
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey('indeed_searches.id'))
    job_title = Column(String)
    company_name = Column(String)
    location = Column(String)
    date_scraped = Column(String)
    date_recorded = Column(String)
    skills = Column(String)
    pay = Column(String)
    job_description = Column(String)
    job_link = Column(String)
    indeed_apply = Column(Boolean)
    search = relationship("IndeedSearch", back_populates="jobs")

# ORM classes for LinkedIn tables
class LinkedInUserProfile(LinkedInBase):
    __tablename__ = 'linkedin_user_profiles'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    # relationships
    job_searches = relationship("LinkedInJobSearch", back_populates="user_profile")

class LinkedInJob(LinkedInBase):
    __tablename__ = 'linkedin_jobs'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('linkedin_user_profiles.id'))
    search_id = Column(Integer, ForeignKey('linkedin_job_searches.id'))
    date_extracted = Column(String)
    date_posted = Column(String)
    job_title = Column(String)
    posted_by = Column(String)
    job_post_link = Column(String)
    job_location = Column(String)
    posted_benefits = Column(String)
    benefit_highlights = Column(String)
    company_highlights = Column(String)
    skills_highlights = Column(String)
    job_post_description = Column(String)

class LinkedInLocation(LinkedInBase):
    __tablename__ = 'linkedin_locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    # Relationships
    job_searches = relationship("LinkedInJobSearch", back_populates="location")

class LinkedInJobSearch(LinkedInBase):
    __tablename__ = 'linkedin_job_searches'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('linkedin_user_profiles.id'))
    search_date = Column(String)
    search_input = Column(String)
    search_results_amount = Column(Integer)
    location_id = Column(Integer, ForeignKey('linkedin_locations.id'))
    
    # Relationships
    user_profile = relationship("LinkedInUserProfile", back_populates="job_searches")
    location = relationship("LinkedInLocation", back_populates="job_searches")

# Dynamically select the database based on a task identifier
def get_engine(task_name):
    if task_name == "Indeed":
        database_path = os.path.join("db", "indeed_db.db")
    elif task_name == "LinkedIn":
        database_path = os.path.join("db", "linkedin_db.db")
    else:
        raise ValueError("Unsupported task name")

    return create_engine(f'sqlite:///{database_path}')

# Create a sessionmaker, dynamically bound to the engine
def get_session(task_name):
    engine = get_engine(task_name)
    Session = sessionmaker(bind=engine)
    return Session  # Return the session class, not an instance

# Method to initialize the database, dynamically based on task
def init_db(task_name):
    engine = get_engine(task_name)
    if task_name == "Indeed":
        print('Initializing Indeed DB')
        IndeedBase.metadata.create_all(engine)  # Only create Indeed tables
    elif task_name == "LinkedIn":
        print('Initializing LinkedIn DB')
        LinkedInBase.metadata.create_all(engine)  # Only create LinkedIn tables
    else:
        raise ValueError("Unsupported task name")
    print(f'{task_name} Database Initialized')


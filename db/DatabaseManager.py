from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
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
    search_entry = Column(String)
    location = Column(String)
    radius = Column(String)
    timestamp = Column(DateTime)
    total_scraped = Column(Integer)
    search_amount = Column(Integer)
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
    date_recorded = Column(String)
    skills = Column(String)
    pay = Column(String)
    job_description = Column(String)
    job_link = Column(String)
    indeed_apply = Column(Boolean)
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

def insert_batch_into_database(batch, db_session):
    """
    Inserts a batch of job listings into the database.

    Args:
        batch (list of dict): A list of dictionaries, each representing a job listing.
    """
    print("Attemtpting to insert Batch")
    print(batch)
    try:
        # Convert each dictionary in the batch to the Job class mapping and add to the session
        db_session.bulk_insert_mappings(Job, batch)
        
        # Commit the transaction
        db_session.commit()
        print(f"Inserted a batch of {len(batch)} records into the database.")
    except SQLAlchemyError as e:
        # Handle any database errors
        print(f"Error during batch insert: {e}")
        db_session.rollback()  # Rollback the transaction in case of error
    except Exception as e:
        print(e)
    
    finally:
        db_session.close()  # Close the session
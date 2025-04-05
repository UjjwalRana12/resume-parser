from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Resume model
class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    similarity_score = Column(Float)
    data = Column(JSON) 

# Create DB engine and session
engine = create_engine('sqlite:///resumes.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

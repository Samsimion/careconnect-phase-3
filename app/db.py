from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the database engine
engine = create_engine('sqlite:///app.db', echo=False)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(bind=engine)

# create_tables.py
from app.models import Base
from app.db import engine

Base.metadata.create_all(engine)
print("All tables created successfully!")

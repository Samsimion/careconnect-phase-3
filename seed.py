from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Doctor, Parent, Patient, Booking
from datetime import datetime

# Set up engine and session
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create doctors
doctor1 = Doctor(name="Dr. Sarah Kim", specialization="Speech Therapist")
doctor2 = Doctor(name="Dr. John Mbele", specialization="Occupational Therapist")

# Create parents
parent1 = Parent(name="Alice Njeri", phone_number="0712345678")
parent2 = Parent(name="Brian Odhiambo", phone_number="0798765432")

# Create patients linked to parents
patient1 = Patient(name="Winnie Njeri", parent=parent1)
patient2 = Patient(name="Derrick Odhiambo", parent=parent2)

# Create bookings
booking1 = Booking(
    parent=parent1,
    doctor=doctor1,
    patient=patient1,
    date=datetime(2025, 6, 10, 10, 0)
)
booking2 = Booking(
    parent=parent2,
    doctor=doctor2,
    patient=patient2,
    date=datetime(2025, 6, 12, 14, 0)
)

# Add all and commit
session.add_all([doctor1, doctor2, parent1, parent2, patient1, patient2, booking1, booking2])
session.commit()

print("✅ Seed data added successfully!")

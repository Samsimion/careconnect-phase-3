from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialization = Column(String)

    bookings = relationship('Booking', back_populates='doctor', cascade='all, delete')

    def __repr__(self):
        return f"<Doctor(name={self.name}, specialization={self.specialization})>"


class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    patients = relationship('Patient', back_populates='parent', cascade='all, delete')
    bookings = relationship('Booking', back_populates='parent', cascade='all, delete')

    def __repr__(self):
        return f"<Parent(name={self.name}, phone={self.phone_number})>"


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)

    parent = relationship('Parent', back_populates='patients')
    bookings = relationship('Booking', back_populates='patient', cascade='all, delete')

    def __repr__(self):
        return f"<Patient(name={self.name}, parent_id={self.parent_id})>"


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False) 
    date = Column(DateTime, default=datetime.utcnow)

    parent = relationship('Parent', back_populates='bookings')
    doctor = relationship('Doctor', back_populates='bookings')
    patient = relationship('Patient', back_populates='bookings')

    def __repr__(self):
        return f"<Booking(date={self.date}, doctor_id={self.doctor_id}, parent_id={self.parent_id}, patient_id={self.patient_id})>"

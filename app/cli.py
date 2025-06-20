from app.models import Doctor, Parent, Patient, Booking
from app.db import SessionLocal
from datetime import datetime
import csv

session = SessionLocal()

def list_doctors():
    doctors = session.query(Doctor).all()
    print("\nAvailable Doctors:")
    for d in doctors:
        print(f"{d.id}. {d.name} - {d.specialization}")

def list_parents():
    parents = session.query(Parent).all()
    print("\nRegistered Parents:")
    for p in parents:
        print(f"{p.id}. {p.name} ({p.phone_number})")

def list_patients():
    patients = session.query(Patient).all()
    print("\nRegistered Patients:")
    for pt in patients:
        parent_name = pt.parent.name if pt.parent else "Unknown"
        print(f"{pt.id}. {pt.name} (Parent: {parent_name})")

def create_booking():
    list_doctors()
    list_parents()
    list_patients()
    
    try:
        doctor_id = int(input("\nEnter doctor ID: "))
        parent_id = int(input("Enter your parent ID: "))
        patient_id = int(input("Enter patient ID (your child): "))
        date_str = input("Enter appointment date (YYYY-MM-DD HH:MM): ")
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

        # yakuprevent ku double book
        conflict = session.query(Booking).filter_by(doctor_id=doctor_id, date=date).first()
        if conflict:
            print("\nError: Doctor already has a booking at that time.")
            return

        booking = Booking(parent_id=parent_id, doctor_id=doctor_id, patient_id=patient_id, date=date)
        session.add(booking)
        session.commit()

        print("\n Booking created successfully!")
        print(f"""
--- Booking Confirmation ---
Date      : {booking.date.strftime('%Y-%m-%d %H:%M')}
Doctor    : {booking.doctor.name}
Patient   : {booking.patient.name}
Parent    : {booking.parent.name}
Phone     : {booking.parent.phone_number}
----------------------------
          
        """)
    except ValueError:
        print("\n Invalid input format. Please try again.")
    except Exception as e:
        print(f"\n Error: {e}")

def view_future_bookings():
    print("\n--- Upcoming Bookings ---")
    now = datetime.now()
    future_bookings = session.query(Booking).filter(Booking.date >= now).order_by(Booking.date).all()
    if not future_bookings:
        print("No upcoming bookings.")
    for b in future_bookings:
        try:
            print(f"{b.date.strftime('%Y-%m-%d %H:%M')} - {b.patient.name} with {b.doctor.name} (Parent: {b.parent.name})")
        except Exception:
            print(" Skipped a booking with missing data.")


def admin_dashboard():
    print("\n--- Admin Dashboard ---")
    bookings = session.query(Booking).order_by(Booking.date).all()
    if not bookings:
        print("No bookings found.")
    for b in bookings:
        try:
            print(f"{b.id}. {b.date.strftime('%Y-%m-%d %H:%M')} - {b.patient.name} with {b.doctor.name} (Parent: {b.parent.name})")
        except Exception:
            print(" Skipped a booking with missing data.")

def export_bookings_to_csv():
    filename = "bookings_export.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Doctor", "Patient", "Parent", "Phone"])
        for b in session.query(Booking).all():
            try:
                writer.writerow([
                    b.date.strftime("%Y-%m-%d %H:%M"),
                    b.doctor.name,
                    b.patient.name,
                    b.parent.name,
                    b.parent.phone_number
                ])
            except Exception:
                continue
    print(f"\n Bookings exported to {filename}")

def add_entity():
    print("\n--- Add New Record ---")
    print("1. Doctor\n2. Parent\n3. Patient")
    choice = input("Choose entity to add: ")

    if choice == "1":
        name = input("Doctor name: ").strip()
        specialization = input("Specialization: ").strip()
        if name and specialization:
            session.add(Doctor(name=name, specialization=specialization))
        else:
            print(" Name and specialization cannot be empty.")
            return
    elif choice == "2":
        name = input("Parent name: ").strip()
        phone = input("Phone number: ").strip()
        if name and phone:
            session.add(Parent(name=name, phone_number=phone))
        else:
            print(" Name and phone number cannot be empty.")
            return
    elif choice == "3":
        name = input("Patient name: ").strip()
        list_parents()
        try:
            parent_id = int(input("Parent ID: "))
            session.add(Patient(name=name, parent_id=parent_id))
        except ValueError:
            print(" Invalid parent ID.")
            return
    else:
        print("Invalid choice.")
        return
    session.commit()
    print("\nRecord added.")

def delete_booking():
    print("\n🗑 Delete a Booking")

    bookings = session.query(Booking).all()
    if not bookings:
        print("No bookings found.")
        return

    for booking in bookings:
        print(f"ID: {booking.id} | Parent: {booking.parent.name} | Doctor: {booking.doctor.name} | Time: {booking.date.strftime('%Y-%m-%d %H:%M')}")

    try:
        booking_id = int(input("Enter the ID of the booking you want to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    booking = session.query(Booking).filter_by(id=booking_id).first()
    if not booking:
        print("Booking not found.")
        return

    confirm = input(f"Are you sure you want to delete this booking (ID {booking.id})? (yes/no): ").lower()
    if confirm == "yes":
        session.delete(booking)
        session.commit()
        print("✅ Booking deleted successfully.")
    else:
        print(" Deletion cancelled.")

def booking_stats():
    print("\nBooking Stats(upcoming)")
    now = datetime.now()
    doctors = session.query(Doctor).all()
    for doc in doctors:
        count = session.query(Booking).filter(Booking.doctor_id == doc.id, Booking.date>=now).count()
        print(f"{doc.name} ({doc.specialization}):{count} upcoming appointments(s)")

def view_my_bookings():
    print("\n=== Parents ===")
    parents = session.query(Parent).all()
    for p in parents:
        print(f"{p.id}. {p.name} ({p.phone_number})")

    try:
        parent_id = int(input("\nEnter your Parent ID to view bookings: "))
        parent = session.query(Parent).get(parent_id)
        if not parent:
            print("Parent not found.")
            return

        print(f"\n📅 Bookings for {parent.name}:")
        if not parent.bookings:
            print("No bookings found.")
        for booking in parent.bookings:
            print(f"- {booking.date.strftime('%Y-%m-%d %H:%M')} | Patient: {booking.patient.name} | Doctor: {booking.doctor.name} ({booking.doctor.specialization})")
    except ValueError:
        print("Invalid input. Please enter a valid Parent ID.")

def view_doctor_appointments():
    print("\n=== Doctors ===")
    doctors = session.query(Doctor).all()
    for d in doctors:
        print(f"{d.id}. Dr. {d.name} ({d.specialization})")

    try:
        doctor_id = int(input("\nEnter your Doctor ID to view appointments: "))
        doctor = session.query(Doctor).get(doctor_id)
        if not doctor:
            print("Doctor not found.")
            return

        print(f"\n📋 Appointments for Dr. {doctor.name}:")
        if not doctor.bookings:
            print("No appointments found.")
        for booking in doctor.bookings:
            print(f"- {booking.date.strftime('%Y-%m-%d %H:%M')} | Patient: {booking.patient.name} | Parent: {booking.parent.name}")
    except ValueError:
        print("Invalid input. Please enter a valid Doctor ID.")




def main():
    while True:
        print("""
=========================
  Welcome to CareConnect
=========================
1. List Doctors
2. List Parents
3. List Patients
4. Book Appointment
5. Admin Dashboard
6. Export Bookings to CSV
7. Add Parent/Doctor/Patient
8. View Upcoming Bookings
9. Delete Booking
10. Booking Stats
11. View My Bookings (Parent)
12. View My Appointments (Doctor)
13. Exit
        """)
        choice = input("Choose an option: ")

        if choice == "1":
            list_doctors()
        elif choice == "2":
            list_parents()
        elif choice == "3":
            list_patients()
        elif choice == "4":
            create_booking()
        elif choice == "5":
            admin_dashboard()
        elif choice == "6":
            export_bookings_to_csv()
        elif choice == "7":
            add_entity()
        elif choice == "8":
            view_future_bookings()
        elif choice == "9":
            delete_booking()

        elif choice == "10":
            booking_stats()
        elif choice == "11":
            view_my_bookings()
        elif choice == "12":
            view_doctor_appointments()
        elif choice == "13":
            print("Goodbye!")
            break
        
            
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    finally:
        session.close()

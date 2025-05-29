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

        # Prevent double booking
        conflict = session.query(Booking).filter_by(doctor_id=doctor_id, date=date).first()
        if conflict:
            print("\n❌ Error: Doctor already has a booking at that time.")
            return

        booking = Booking(parent_id=parent_id, doctor_id=doctor_id, patient_id=patient_id, date=date)
        session.add(booking)
        session.commit()

        print("\n✅ Booking created successfully!")
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
        print("\n❌ Invalid input format. Please try again.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

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
            print("⚠️ Skipped a booking with missing data.")

def delete_booking():
    print("\n--- Delete a Booking ---")
    view_future_bookings()
    try:
        booking_id = int(input("\nEnter Booking ID to delete: "))
        booking = session.query(Booking).get(booking_id)
        if not booking:
            print("❌ Booking not found.")
            return
        session.delete(booking)
        session.commit()
        print("✅ Booking deleted successfully.")
    except ValueError:
        print("❌ Invalid ID format.")
    except Exception as e:
        print(f"❌ Error: {e}")

def admin_dashboard():
    print("\n--- Admin Dashboard ---")
    bookings = session.query(Booking).order_by(Booking.date).all()
    if not bookings:
        print("No bookings found.")
    for b in bookings:
        try:
            print(f"{b.id}. {b.date.strftime('%Y-%m-%d %H:%M')} - {b.patient.name} with {b.doctor.name} (Parent: {b.parent.name})")
        except Exception:
            print("⚠️ Skipped a booking with missing data.")

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
    print(f"\n✅ Bookings exported to {filename}")

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
            print("❌ Name and specialization cannot be empty.")
            return
    elif choice == "2":
        name = input("Parent name: ").strip()
        phone = input("Phone number: ").strip()
        if name and phone:
            session.add(Parent(name=name, phone_number=phone))
        else:
            print("❌ Name and phone number cannot be empty.")
            return
    elif choice == "3":
        name = input("Patient name: ").strip()
        list_parents()
        try:
            parent_id = int(input("Parent ID: "))
            session.add(Patient(name=name, parent_id=parent_id))
        except ValueError:
            print("❌ Invalid parent ID.")
            return
    else:
        print("Invalid choice.")
        return
    session.commit()
    print("\n✅ Record added.")

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
10. Exit
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
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

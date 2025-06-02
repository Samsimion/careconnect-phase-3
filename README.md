# CareConnect CLI – Phase 3

**CareConnect CLI** is a command-line application designed to assist parents in booking therapy sessions for their children with specialized doctors. This tool aims to streamline the appointment process and enhance accessibility to care.

## 🚀 Features

- **Doctor Management**: Register and list doctors with their specializations.
- **Parent & Patient Management**: Add and view parent and patient details.
- **Appointment Booking**: Schedule sessions between patients and doctors.
- **Conflict Prevention**: Avoid double-booking for the same time slot.
- **Booking Overview**: View upcoming and all bookings.
- **Data Export**: Export booking data to CSV format.
- **Administrative Tools**: Dashboard for managing and deleting bookings.
- **Statistics**: View booking statistics per doctor.

##  Technologies Used

- **Python 3**
- **SQLAlchemy ORM**
- **SQLite** (lightweight database)
- **Datetime** module
- **CSV** module for data export

##  Project Structure

careconnect-phase-3/
├── app/
│ ├── init.py
│ ├── models.py # SQLAlchemy ORM models
│ └── db.py # Database setup and session management
├── migrations/ # Alembic migration files
├── bookings_export.csv # Exported bookings data
├── alembic.ini # Alembic configuration
├── cli.py # Main CLI application
├── seed.py # Script to populate the database with initial data
├── app.db # SQLite database file
├── Pipfile # Project dependencies
├── Pipfile.lock # Locked versions of dependencies
└── README.md # Project documentation

bash
Copy
Edit

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Samsimion/careconnect-phase-3.git
cd careconnect-phase-3
2. Install Dependencies
Ensure you have Pipenv installed. Then run:

bash
Copy
Edit
pipenv install
3. Activate the Virtual Environment
bash
Copy
Edit
pipenv shell
4. Initialize the Database
bash
Copy
Edit
python seed.py
This script will create the database and populate it with initial data.

5. Run the Application
bash
Copy
Edit
pipenv run python -m app.cli
Follow the on-screen prompts to interact with the application.

 Sample Data
The seed.py script adds sample doctors, parents, patients, and bookings to the database for testing purposes.

Future Enhancements
Authentication: Implement user authentication for parents and admins.

Email Notifications: Send email confirmations upon booking.

Web Interface: Develop a web-based frontend for broader accessibility.

Calendar Integration: Sync bookings with calendar applications.

 Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

 License
This project is licensed under the MIT License.


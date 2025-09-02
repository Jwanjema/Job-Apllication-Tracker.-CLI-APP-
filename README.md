A command-line interface (CLI) application for tracking job applications built with Python and SQLAlchemy.

## Features
Add New Applications: Record job title, company, application date, status, deadline, and notes

View All Applications: See all your job applications in a clean, organized format

Update Application Status: Change the status of any application (Applied, Interviewing, Offer, Rejected, Accepted, Withdrawn)

Delete Applications: Remove applications you no longer want to track

Search Applications: Find applications by company name or job title

Company Statistics: View application statistics grouped by company

Persistence: All data is stored in a SQLite database using SQLAlchemy ORM

## Installation
Clone or download this repository

Navigate to the project directory

Install the required dependencies:

### bash
pip install sqlalchemy
## Project Structure
Job-Apllication-Tracker.-CLI-APP-/
│
├── main.py          # Main application entry point
├── models.py        # SQLAlchemy ORM models
├── database.py      # Database operations and session management
├── utils.py         # Helper functions and utilities
└── README.md        # This file
## How to Use
Run the application:

## bash
python main.py
You'll see the main menu:

==================================================
      JOB APPLICATION TRACKER
==================================================
1. Add a new application
2. View all applications
3. Update application status
4. Delete an application
5. Search applications
6. View companies
7. Exit
==================================================
Select an option by entering the corresponding number (1-7)

Follow the prompts to complete your desired action

## Database
The application uses SQLite with SQLAlchemy ORM for data persistence. All data is stored in a local file called job_applications.db that is automatically created when you first run the application.

## Status Options
Applications can have one of the following statuses:
Applied
Interviewing
Offer
Rejected
Accepted
Withdrawn

## Author
Joe Wanjema

License
This project is for educational purposes.

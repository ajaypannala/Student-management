# Student Management System

A command-line Student Management Application built in Python, demonstrating:

- **Variables & Functions** – core program logic organized into small, reusable functions
- **Object-Oriented Programming** – `Student` and `StudentManager` classes encapsulating data and behavior
- **File Handling** – student records persisted to disk as JSON (`data/students.json`)
- **Exception Handling** – custom exceptions (`StudentNotFoundError`, `DuplicateStudentError`, `InvalidDataError`) plus defensive handling of I/O and input errors
- **Git Version Control** – the project history itself shows incremental, real-world development

## Features

- Add a student
- View all students
- Search a student by ID
- Update a student's details
- Delete a student
- Automatic save/load from a JSON file
- Input validation with clear error messages

## Requirements

Python 3.8+. No third-party packages required (standard library only).

## Usage

```bash
python student_manager.py
```

Follow the on-screen menu to add, view, search, update, or delete student records.
Data is automatically saved to `data/students.json` after every change and reloaded
on the next run.

## Project Structure

```
student_management_system/
├── student_manager.py   # Main application (models, manager, CLI)
├── data/
│   └── students.json    # Persisted student records (created automatically)
└── README.md
```

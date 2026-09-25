"""
Student Management System
--------------------------
A command-line application to manage student records, demonstrating
variables, functions, OOP, file handling, and exception handling.
"""

import json
import os


class StudentNotFoundError(Exception):
    """Raised when a requested student ID does not exist in the records."""
    pass


class DuplicateStudentError(Exception):
    """Raised when trying to add a student ID that already exists."""
    pass


class InvalidDataError(Exception):
    """Raised when student data fails validation."""
    pass


class Student:
    """Represents a single student record."""

    def __init__(self, student_id, name, age, grade, email):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email

    def to_dict(self):
        """Convert the Student object into a plain dict (for JSON storage)."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Student object from a dict (loaded from JSON)."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            grade=data["grade"],
            email=data["email"],
        )

    def __str__(self):
        return (f"ID: {self.student_id} | Name: {self.name} | Age: {self.age} "
                f"| Grade: {self.grade} | Email: {self.email}")


class StudentManager:
    """Handles CRUD operations and JSON file persistence for students."""

    def __init__(self, data_file="data/students.json"):
        self.data_file = data_file
        self.students = {}  # student_id -> Student
        self.load_from_file()

    # ---------- File Handling ----------

    def load_from_file(self):
        """Load students from the JSON file, if it exists."""
        if not os.path.exists(self.data_file):
            self.students = {}
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            self.students = {
                sid: Student.from_dict(record) for sid, record in raw_data.items()
            }
        except json.JSONDecodeError:
            print(f"Warning: '{self.data_file}' is corrupted or empty. "
                  "Starting with an empty student list.")
            self.students = {}
        except (OSError, IOError) as e:
            print(f"Warning: could not read '{self.data_file}' ({e}). "
                  "Starting with an empty student list.")
            self.students = {}

    def save_to_file(self):
        """Persist the current student records to the JSON file."""
        os.makedirs(os.path.dirname(self.data_file) or ".", exist_ok=True)
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                data = {sid: student.to_dict() for sid, student in self.students.items()}
                json.dump(data, f, indent=4)
        except (OSError, IOError) as e:
            print(f"Error: could not save data to '{self.data_file}' ({e}).")

    # ---------- CRUD Operations ----------

    def add_student(self, student_id, name, age, grade, email):
        if student_id in self.students:
            raise DuplicateStudentError(f"Student ID '{student_id}' already exists.")
        if not name.strip():
            raise InvalidDataError("Student name cannot be empty.")
        if not isinstance(age, int) or age <= 0:
            raise InvalidDataError("Age must be a positive integer.")

        self.students[student_id] = Student(student_id, name, age, grade, email)
        self.save_to_file()

    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError(f"No student found with ID '{student_id}'.")
        return self.students[student_id]

    def update_student(self, student_id, **kwargs):
        student = self.get_student(student_id)  # raises StudentNotFoundError if missing
        for field, value in kwargs.items():
            if value is not None and hasattr(student, field):
                setattr(student, field, value)
        self.save_to_file()

    def delete_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError(f"No student found with ID '{student_id}'.")
        del self.students[student_id]
        self.save_to_file()

    def list_students(self):
        return list(self.students.values())


# ---------- CLI Helper Functions ----------

MENU_TEXT = """
========= Student Management System =========
1. Add a student
2. View all students
3. Search student by ID
4. Update a student
5. Delete a student
6. Exit
===============================================
"""


def prompt_int(prompt_text):
    """Prompt the user for an integer, re-asking on invalid input."""
    while True:
        try:
            return int(input(prompt_text).strip())
        except ValueError:
            print("Please enter a valid whole number.")


def add_student_flow(manager):
    print("\n--- Add New Student ---")
    student_id = input("Student ID: ").strip()
    name = input("Name: ").strip()
    age = prompt_int("Age: ")
    grade = input("Grade/Class: ").strip()
    email = input("Email: ").strip()

    try:
        manager.add_student(student_id, name, age, grade, email)
        print(f"Student '{name}' added successfully.")
    except (DuplicateStudentError, InvalidDataError) as e:
        print(f"Error: {e}")


def view_students_flow(manager):
    print("\n--- All Students ---")
    students = manager.list_students()
    if not students:
        print("No student records found.")
        return
    for student in students:
        print(student)


def search_student_flow(manager):
    print("\n--- Search Student ---")
    student_id = input("Enter Student ID: ").strip()
    try:
        student = manager.get_student(student_id)
        print(student)
    except StudentNotFoundError as e:
        print(f"Error: {e}")


def update_student_flow(manager):
    print("\n--- Update Student ---")
    student_id = input("Enter Student ID to update: ").strip()
    try:
        manager.get_student(student_id)  # confirm existence first
    except StudentNotFoundError as e:
        print(f"Error: {e}")
        return

    print("Leave a field blank to keep its current value.")
    name = input("New Name: ").strip() or None
    age_input = input("New Age: ").strip()
    age = int(age_input) if age_input.isdigit() else None
    grade = input("New Grade/Class: ").strip() or None
    email = input("New Email: ").strip() or None

    try:
        manager.update_student(student_id, name=name, age=age, grade=grade, email=email)
        print("Student updated successfully.")
    except (StudentNotFoundError, InvalidDataError) as e:
        print(f"Error: {e}")


def delete_student_flow(manager):
    print("\n--- Delete Student ---")
    student_id = input("Enter Student ID to delete: ").strip()
    try:
        manager.delete_student(student_id)
        print("Student deleted successfully.")
    except StudentNotFoundError as e:
        print(f"Error: {e}")


def main():
    manager = StudentManager()

    while True:
        print(MENU_TEXT)
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                add_student_flow(manager)
            elif choice == "2":
                view_students_flow(manager)
            elif choice == "3":
                search_student_flow(manager)
            elif choice == "4":
                update_student_flow(manager)
            elif choice == "5":
                delete_student_flow(manager)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting safely.")
            break
        except Exception as e:
            # Catch-all safety net so one bad operation never crashes the app
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

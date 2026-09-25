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

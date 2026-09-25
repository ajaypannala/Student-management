"""
Student Management System
--------------------------
A command-line application to manage student records, demonstrating
variables, functions, OOP, file handling, and exception handling.
"""


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

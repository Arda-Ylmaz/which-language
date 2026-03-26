"""
SPECS test scenarios
Project: mini-grades (v1)
"""

import subprocess
import os
import shutil
import pytest

# --- Helper Functions ---
def run_cmd(args):
    """Executes the command in the terminal. Runs 'init' first to ensure the system is always ready."""
    # Automatically prepare the system at the start of each test
    subprocess.run(["python", "solution.py", "init"], capture_output=True, text=True)
    
    result = subprocess.run(
        ["python", "solution.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def setup_function():
    """Resets the .minigrades directory before each test."""
    if os.path.exists(".minigrades"):
        shutil.rmtree(".minigrades")

# --- add student tests ---
def test_add_student_success():
    """Tests the successful addition of a new student with a unique ID."""
    response = run_cmd(["add", "101", "Berke"])
    assert response == "Student added successfully."

def test_add_student_duplicate():
    """Tests the 'Duplicate ID' error when attempting to add a student with an existing ID."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["add", "101", "Efe"])
    assert response == "Error: Student with ID 101 already exists."

def test_add_student_non_numeric_id():
    """Tests the numeric value error when a non-numeric string is entered as an ID."""
    response = run_cmd(["add", "abc", "Berke"])
    assert response == "Invalid input: Please enter a numeric value."

# --- add grade tests ---
def test_add_grade_success():
    """Tests the successful addition of valid grades to an existing student."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["add-grade", "101", "80"])
    assert response == "Grades added successfully for student 101."

def test_add_grade_non_numeric_grade():
    """Tests that the added grade must consist of numbers."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["add-grade", "101", "abc"])
    assert response == "Invalid input: Please enter a numeric value."

def test_add_grade_student_not_found():
    """Tests the error when trying to add a grade to a student ID that does not exist."""
    response = run_cmd(["add-grade", "999", "80"])
    assert response == "Error: No student found with ID 999."

def test_add_grade_out_of_range():
    """Tests that the added grade must be between 0 and 100."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["add-grade", "101", "101"])
    assert response == "Invalid grade: Grades must be between 0 and 100."

# --- delete student tests ---
def test_delete_student_success():
    """Tests the deletion of an existing student via their ID."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["delete", "101"])
    assert response == "Student and all grades deleted successfully."

def test_delete_student_not_found():
    """Tests the error message when attempting to delete a non-existent ID."""
    response = run_cmd(["delete", "999"])
    assert response == "Error: No student found with ID 999."

# --- delete grade tests ---
def test_delete_grade_success():
    """Tests the deletion of an existing grade for student via their ID."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add-grade", "101", "85"])
    response = run_cmd(["del-grade", "101", "85"])
    assert response == "Grade 85 successfully removed!"

def test_delete_grade_non_numeric_id():
    """Tests that the added grade must consist of numbers."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add-grade", "101", "85"])
    response = run_cmd(["del-grade", "abc", "85"])
    assert response == "Invalid input: Please enter a numeric value."

def test_delete_grade_non_numeric_grade():
    """Tests that the added grade must consist of numbers."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add-grade", "101", "85"])
    response = run_cmd(["del-grade", "101", "abc"])
    assert response == "Invalid input: Please enter a numeric value."

def test_delete_grade_out_of_range():
    """Tests that the added grade must be between 0 and 100."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add-grade", "101", "85"])
    response = run_cmd(["del-grade", "101", "101"])
    assert response == "Invalid grade: Grades must be between 0 and 100."

def test_delete_grade_student_not_found():
    """Tests the error when trying to delete a grade from a student ID that does not exist."""
    response = run_cmd(["del-grade", "999", "85"])
    assert response == "Error: No student found with ID 999."

def test_delete_grade_not_found():
    """Tests the error when trying to delete a grade that does not exist."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add-grade", "101", "85"])
    response = run_cmd(["del-grade", "101", "90"])
    assert response == "Error: Grade 90 not found for this student."

# --- calculate average tests ---
def test_calculate_average_success():
    """Tests the (simulation message) for a registered student's average calculation."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add-grade", "101", "85"])
    response = run_cmd(["calc-avg", "101"])
    assert response == "Average for student 101 is 85.00."

def test_calculate_average_student_not_found():
    """Tests the error when querying the average of a non-registered student."""
    response = run_cmd(["calc-avg", "999"])
    assert response == "Error: No student found with ID 999."

def test_could_not_calculate_average():
    """Tests the error when querying the average of a non-registered student."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["calc-avg", "101"])
    assert response == "Error: Could not calculate average for student 101."

# --- list students tests ---
def test_list_students_success():
    """Tests the listing of all registered students according to the format (ID | Name)."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add", "102", "Efe"])
    response = run_cmd(["list"])
    assert "=== LIST OF STUDENTS ===" in response
    assert " " in response
    assert "Student 1" in response
    assert "---------------" in response
    assert "ID: 101" in response
    assert "Name: Berke" in response
    assert "Grades: None" in response
    assert "Error: Could not calculate average for student 101." in response
    assert "---------------" in response
    assert " " in response
    assert "Student 2" in response
    assert "---------------" in response
    assert "ID: 102" in response
    assert "Name: Efe" in response
    assert "Grades: None" in response
    assert "Error: Could not calculate average for student 102." in response
    assert "---------------" in response

def test_list_students_with_grades_success():
    """Tests the listing of all registered students according to the format (ID | Name | Grades)."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add-grade", "101", "85"])
    run_cmd(["add", "102", "Eren"])
    run_cmd(["add-grade", "102", "90"])
    response = run_cmd(["list"])
    assert "=== LIST OF STUDENTS ===" in response
    assert " " in response
    assert "Student 1" in response
    assert "---------------" in response
    assert "ID: 101" in response
    assert "Name: Berke" in response
    assert "Grades: 85" in response
    assert "Average for student 101 is 85.00." in response
    assert "---------------" in response
    assert " " in response
    assert "Student 2" in response
    assert "ID: 102" in response
    assert "Name: Eren" in response
    assert "Grades: 90" in response
    assert "Average for student 102 is 90.00." in response
    assert "---------------" in response

def test_list_students_empty():
    """Tests the error when listing is requested while no students are registered."""
    response = run_cmd(["list"])
    assert response == "Error: No students found in the system. Operation aborted."

# --- generate report tests ---
def test_generate_report_success():
    """Tests the successful generation of a report from system data."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add", "102", "Efe"])
    response = run_cmd(["report"])
    assert response == "Report saved to .minigrades/report.txt"
    assert os.path.exists(".minigrades/report.txt")

def test_generate_report_empty():
    """Tests the error when report generation is requested with no registered students."""
    response = run_cmd(["report"])
    assert response == "Error: No data available to generate a report."

# --- unknown command test ---
def test_unknown_command():
    """Tests the error provided when an unknown command is entered."""
    response = run_cmd(["hello"])
    assert "Unknown command: hello. Please select from the menu." in response

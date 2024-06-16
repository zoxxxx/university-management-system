import mysql.connector
import pandas as pd

def add_enrollment(student_id: str, course_id: int, semester: str, db):

    try:
        with db.cursor() as cursor:
            cursor.execute(
                "CALL RegisterCourse(%s, %s, %s)", 
                (student_id, course_id, semester)
            )
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def delete_enrollment(enrollment_id: int, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Enrollment WHERE EnrollmentID = %s",
                (str(enrollment_id),)
            )
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def get_student_enrollments(student_id: str, db):
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT e.EnrollmentID, c.CourseName, e.Semester, e.Grade
                FROM Enrollment e
                JOIN Course c ON e.CourseID = c.CourseID
                WHERE e.StudentID = %s
            """
            cursor.execute(query, (str(student_id),))
            enrollments = cursor.fetchall()
            return pd.DataFrame(enrollments)
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"General error: {e}")
        return pd.DataFrame()

def get_all_enrollments(db):
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT e.EnrollmentID, s.StudentID, s.Name as StudentName, c.CourseName, e.Semester, e.Grade
                FROM Enrollment e
                JOIN Course c ON e.CourseID = c.CourseID
                JOIN Student s ON e.StudentID = s.StudentID
            """
            cursor.execute(query)
            enrollments = cursor.fetchall()
            return pd.DataFrame(enrollments)
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"General error: {e}")
        return pd.DataFrame()

def update_enrollment_grade(enrollment_id: int, grade: int, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "UPDATE Enrollment SET Grade=%s WHERE EnrollmentID=%s",
                (str(grade), str(enrollment_id))
            )
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

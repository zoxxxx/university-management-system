import mysql.connector
import pandas as pd

def add_major(major_name: str, college_id: int, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Major (MajorName, CollegeID) VALUES (%s, %s)",
                (major_name, str(college_id))
            )
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def get_all_majors(db):
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT MajorID, MajorName, CollegeName, StudentCount FROM Major JOIN College ON Major.CollegeID = College.CollegeID")
            majors = cursor.fetchall()
            return pd.DataFrame(majors)
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()

def delete_major(major_id: int, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM Major WHERE MajorID = %s", (str(major_id),))
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def get_major_by_student_id(student_id: str, db):
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT MajorName, Major.MajorID FROM Major JOIN Student ON Major.MajorID = Student.MajorID WHERE StudentID = %s",
                (student_id,)
            )
            major = cursor.fetchone()
            return major
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None
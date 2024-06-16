import mysql.connector
import pandas as pd

def add_course(course_name: str, credits: int, offering_college_id: int, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Course (CourseName, Credits, OfferingCollegeID) VALUES (%s, %s, %s)",
                (course_name, credits, offering_college_id)
            )
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def get_all_courses(db):
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT c.CourseID, c.CourseName, c.Credits, cl.CollegeName FROM Course c JOIN College cl ON c.OfferingCollegeID = cl.CollegeID")
            courses = cursor.fetchall()
            return pd.DataFrame(courses)
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"General error: {e}")
        return pd.DataFrame()

def delete_course(course_id: int, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM Course WHERE CourseID = %s", (str(course_id),))
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

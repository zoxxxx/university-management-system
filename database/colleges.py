import mysql.connector
import pandas as pd

def add_college(college_name: str, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO College (CollegeName) VALUES (%s)",
                (college_name,)
            )
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def get_all_colleges(db):
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT CollegeID, CollegeName FROM College")
            colleges = cursor.fetchall()
            return pd.DataFrame(colleges)
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()

def delete_college(college_id: int, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM College WHERE CollegeID = %s", (str(college_id),))
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

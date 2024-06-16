import mysql.connector
import pandas as pd

def change_major(student_id: str, new_major_id: int, change_date: str, db):
    try:
        with db.cursor() as cursor:
            # cursor.execute(
            #     "INSERT INTO MajorChange (StudentID, NewMajorID, ChangeDate) VALUES (%s, %s, %s)",
            #     (student_id, new_major_id, change_date)
            # )
            # db.commit()
            # return True
            cursor.execute(
                "CALL ChangeStudentMajor(%s, %s, %s)", (student_id, new_major_id, change_date))
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def get_all_majorchanges(db):
    """
    Retrieves all major change records from the database.
    
    Args:
    db: mysql.connector.connection
        The database connection object.
    
    Returns:
    DataFrame
        A DataFrame containing all major changes.
    """
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT mc.ChangeID, mc.StudentID, s.Name as StudentName, m.MajorName as NewMajor, mc.ChangeDate
                FROM MajorChange mc
                JOIN Student s ON mc.StudentID = s.StudentID
                JOIN Major m ON mc.NewMajorID = m.MajorID
            """)
            changes = cursor.fetchall()
            return pd.DataFrame(changes)
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()
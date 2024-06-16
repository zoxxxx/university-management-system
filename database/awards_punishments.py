import mysql.connector
import pandas as pd

def get_student_awards_punishments(student_id, db):
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM AwardPunishment WHERE StudentId = %s", (student_id, ))
            awards_punishments = cursor.fetchall()
            return pd.DataFrame(awards_punishments)
    except Exception as e:
        print(f"Error getting AwardPunishment: {e}")
        return pd.DataFrame()

def add_award_punishment(student_id, award_punishment, date, description, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("INSERT INTO AwardPunishment (StudentId, Type, Description, Date) VALUES (%s, %s, %s, %s)", (student_id, award_punishment, description, date))
            db.commit()
            return True
    except Exception as e:
        print(f"Error adding AwardPunishment: {e}")
        return False

def delete_award_punishment(apid, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM AwardPunishment WHERE APID = %s", (str(apid), ))
            db.commit()
            return True
    except Exception as e:
        print(f"Error deleting AwardPunishment: {e}")
        return False

def get_all_awards_punishments(db):
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT a.APID, a.StudentID, s.Name, a.Type, a.Description, a.Date 
                            FROM AwardPunishment a
                            JOIN Student s ON a.StudentID = s.StudentID""")
            awards_punishments = cursor.fetchall()
            return pd.DataFrame(awards_punishments)
    except Exception as e:
        print(f"Error getting all AwardPunishment: {e}")
        return pd.DataFrame()
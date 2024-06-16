import hashlib
import mysql.connector

def create_user(username :str, hashed_password : str, role : str, db, student_id : str) -> bool:
    try:
        with db.cursor() as cursor:
            if role == "student":
                cursor.execute("INSERT INTO account (username, password, role, StudentId) VALUES (%s, %s, %s, %s)", (username, hashed_password, role, student_id))
            else:
                cursor.execute("INSERT INTO account (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
            db.commit()
            return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def verify_user(username : str, hashed_password : str, db) -> str:
    print(f"Verifying user {username}")
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT password, role FROM account WHERE username = %s", (username, ))
            user_info = cursor.fetchone()
            
            if user_info is None:
                print ("User not found")
                return None
            if user_info and hashed_password == user_info[0]:
                return user_info[1]  # 返回用户角色
            print ("Password incorrect")
            return None
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None

def get_student_id(username : str, db) -> str:
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT StudentId FROM account WHERE username = %s", (username, ))
            student_id = cursor.fetchone()[0]
            return student_id
    except Exception as e:
        print(f"Error getting student id: {e}")
        return None

def get_user_role(username : str, db) -> str:
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT role FROM account WHERE username = %s", (username, ))
            role = cursor.fetchone()[0]
            return role
    except Exception as e:
        print(f"Error getting user role: {e}")
        return None
import mysql.connector
import pandas as pd

def get_all_students(db):
    try:
        with db.cursor(dictionary=True) as cursor:
            # 执行查询所有学生的SQL语句并调用计算加权平均成绩的函数
            cursor.execute("""
                SELECT 
                    Student.StudentID, 
                    Student.Name, 
                    Student.Gender, 
                    Student.DateOfBirth, 
                    Student.ContactInfo, 
                    Student.EnrollmentYear, 
                    Major.MajorName,
                    CalculateWeightedAverageGrade(Student.StudentID) AS WeightedAverageGrade
                FROM 
                    Student
                JOIN 
                    Major ON Student.MajorID = Major.MajorID
            """)
            # 获取所有学生的记录
            students = cursor.fetchall()
            return pd.DataFrame(students)
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()  # 返回空DataFrame以保持一致性
    except Exception as e:
        print(f"General error: {e}")
        return pd.DataFrame()  # 返回空DataFrame以保持一致性


def update_student(student_id, name, gender, date_of_birth, contact_info, enrollment_year, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "UPDATE Student SET Name=%s, Gender=%s, DateOfBirth=%s, ContactInfo=%s, EnrollmentYear=%s WHERE StudentID=%s",
                (name, gender, date_of_birth, contact_info, enrollment_year, student_id))
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def add_student(student_id, name, gender, date_of_birth, contact_info, enrollment_year, major_id, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Student (StudentID, Name, Gender, DateOfBirth, ContactInfo, EnrollmentYear, MajorID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (student_id, name, gender, date_of_birth, contact_info, enrollment_year, major_id))
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def delete_student(student_id, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM Student WHERE StudentID=%s", (student_id,))
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def upload_image(student_id, image_data, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE Student SET Photo=%s WHERE StudentID=%s", (image_data, student_id))
            db.commit()
            return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def get_student_image(student_id, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT Photo FROM Student WHERE StudentID=%s", (student_id,))
            image_data = cursor.fetchone()
            return image_data[0] if image_data else None
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None

def get_student_info(student_id, db):
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT StudentID,
                                    Name,
                                    Gender,
                                    DateOfBirth,
                                    ContactInfo,
                                    EnrollmentYear,
                                    Major.MajorName AS MajorName,
                                    CalculateWeightedAverageGrade(StudentID) AS WeightedAverageGrade
                                FROM Student
                                JOIN Major ON Student.MajorID = Major.MajorID
                                WHERE StudentID = %s""", (student_id,))
            student_info = cursor.fetchone()
            return student_info
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None
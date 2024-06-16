# import database.students
from database import students
import frontend.utils
import streamlit as st
import pandas as pd
import datetime

def show():
    frontend.utils.show_sidebar()
    st.title("我的信息")
    st.write("")
    st.write("")
    student_id = st.session_state.get("student_id")
    if student_id is None:
        st.error("请先登录")
        return
    
    student = students.get_student_info(student_id, st.session_state.db_connection)
    if student is None:
        st.error("学生信息不存在")
        return
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
        st.text_input("学号", value=student['StudentID'], disabled=True)
        name = st.text_input("姓名", value=student['Name'], disabled=True)
        gender = st.selectbox("性别", ["男", "女", "其他"], index=["男", "女", "其他"].index(student['Gender']))
        date_of_birth = st.date_input("生日", value=pd.to_datetime(student['DateOfBirth']), min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
        contact_info = st.text_input("电话", value=student['ContactInfo'])
        enrollment_year = st.number_input("入学年份", value=int(student['EnrollmentYear']), step=1, min_value=1900, max_value=2100)
        st.text_input("专业", value=student['MajorName'], disabled=True)


        is_success = False
        is_fail = False

        if st.button("修改", type="primary"):
            if(students.update_student(
                student['StudentID'], 
                name,
                gender,
                date_of_birth,
                contact_info,
                enrollment_year,
                db=st.session_state.db_connection
            )):
                is_success = True
            else:
                is_fail = True
            
            if is_success:
                st.success("修改成功")
            elif is_fail:
                st.error("修改失败")

    with col2:
        image = students.get_student_image(student_id, st.session_state.db_connection)
        if image is not None:
            st.image(image, width=400)
        uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            if students.upload_image(student_id, uploaded_file, st.session_state.db_connection):
                st.success("上传成功")
            else:
                st.error("上传失败")
        
    st.write(f"# 加权平均分: {student['WeightedAverageGrade']}")

show()
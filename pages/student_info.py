from database import students, awards_punishments, enrollments, courses, majors, majorchanges
import frontend.utils
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
import datetime

@st.experimental_dialog("修改学生信息")
def edit_student_dialog(student):
    st.write("修改学号为", student['StudentID'], "的学生信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    name = st.text_input("姓名", value=student['Name'])
    gender = st.selectbox("性别", ["男", "女", "其他"], index=["男", "女", "其他"].index(student['Gender']))
    date_of_birth = st.date_input("生日", value=pd.to_datetime(student['DateOfBirth']), min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    contact_info = st.text_input("电话", value=student['ContactInfo'])
    enrollment_year = st.number_input("入学年份", value=int(student['EnrollmentYear']), step=1, min_value=1900, max_value=2100)
    major = majors.get_major_by_student_id(student['StudentID'], st.session_state.db_connection)
    st.text_input("专业", value=major['MajorName'], disabled=True)
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False
    is_fail = False

    with col1:
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
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("成功修改学生信息")
    if is_fail:
        st.error("修改学生信息失败")

@st.experimental_dialog("添加学生")
def add_student_dialog():
    st.write("添加学生信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    student_id = st.text_input("学号")
    name = st.text_input("姓名")
    gender = st.selectbox("性别", ["男", "女", "其他"])
    date_of_birth = st.date_input("生日", min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    contact_info = st.text_input("电话")
    enrollment_year = st.number_input("入学年份", step=1, min_value=1900, max_value=2100, value=2021)

    major_options = majors.get_all_majors(st.session_state.db_connection)
    major_options = dict(zip(major_options['MajorName'], major_options['MajorID']))
    major = st.selectbox("专业", list(major_options.keys()))
    major_id = major_options[major]

    col1, _, col2 = st.columns([1, 1, 1])


    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(students.add_student(
                student_id=student_id,
                name=name,
                gender=gender,
                date_of_birth=date_of_birth,
                contact_info=contact_info,
                enrollment_year=enrollment_year,
                major_id=major_id,
                db=st.session_state.db_connection
            )):
                is_success = True
            else:
                is_fail = True
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("成功添加学生")
    if is_fail:
        st.error("添加学生失败")


@st.experimental_dialog("删除学生")
def delete_student_dialog(student):
    st.write("删除学号为", student['StudentID'], "的学生信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)

    is_success = False
    is_fail = False

    col1, _, col2 = st.columns([1, 1, 1])
    with col1:
        if st.button("删除", type="primary"):
            if(students.delete_student(student['StudentID'], db=st.session_state.db_connection)):
                is_success = True
            else :
                is_fail = True

    with col2:
        if st.button("取消"):
            st.rerun()

    if is_success:
        st.success("成功删除学生")
    if is_fail:
        st.error("删除学生失败")

@st.experimental_dialog("查看学生奖惩信息")
def show_student_rewards_punishments(student):
    st.write("学号为", student['StudentID'], "的学生奖惩信息")
    df = awards_punishments.get_student_awards_punishments(student['StudentID'], st.session_state.db_connection)
    if df.empty:
        st.write("该学生没有奖惩信息")
    else:
        st.write(df)

@st.experimental_dialog("添加奖惩信息")
def add_award_punishment_dialog(student):
    st.write("添加奖惩信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    st.text_input("学号", value=student['StudentID'], disabled=True)
    award_punishment = st.selectbox("奖惩", ["奖", "惩"])
    award_punishment_date = st.date_input("日期", min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    award_punishment_reason = st.text_area("原因")
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(awards_punishments.add_award_punishment(
                student_id=student['StudentID'],
                award_punishment=award_punishment,
                date=award_punishment_date,
                description=award_punishment_reason,
                db=st.session_state.db_connection
            )):
                is_success = True
            else:
                is_fail = True
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("添加成功")
    if is_fail:
        st.error("添加失败")

@st.experimental_dialog("查看学生选课信息")
def show_student_enrollments(student):
    st.write("学号为", student['StudentID'], "的学生选课信息")
    
    df = enrollments.get_student_enrollments(student['StudentID'], st.session_state.db_connection)
    if df.empty:
        st.write("该学生没有选课信息")
    else:
        st.write(df)

@st.experimental_dialog("添加选课信息")
def add_enrollment_dialog(student):
    st.write("添加选课信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    student_id = st.text_input("学号", value=student['StudentID'], disabled=True)
    df = courses.get_all_courses(st.session_state.db_connection)
    # course_options = "("df['CourseID'] + ") " + df['Name']
    course_options = dict(zip([f"({df.iloc[i]['CourseID']})  {df.iloc[i]['CourseName']}" for i in range(len(df))], df["CourseID"]))
    course_id = st.selectbox("课程", course_options.keys())
    course_id = course_options[course_id]
    semester = st.selectbox("学期", ["2020春季", "2020秋季", "2021春季", "2021秋季", "2022春季", "2022秋季", "2023春季", "2023秋季", "2024春季", "2024秋季", "2025春季", "2025秋季"])

    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(enrollments.add_enrollment(
                student_id=student_id,
                course_id=course_id,
                semester=semester,
                db=st.session_state.db_connection
            )):
                is_success = True
            else:
                is_fail = True
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("添加成功")
    if is_fail:
        st.error("添加失败")

@st.experimental_dialog("修改专业信息")
def edit_major_dialog(student):
    st.write("修改专业信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)

    major = majors.get_major_by_student_id(student['StudentID'], st.session_state.db_connection)
    st.text_input("学号", value=student['StudentID'], disabled=True)
    st.text_input("专业", value=major['MajorName'], disabled=True)
    major_options = majors.get_all_majors(st.session_state.db_connection)
    major_options = dict(zip(major_options['MajorName'], major_options['MajorID']))
    major = st.selectbox("新专业", list(major_options.keys()))
    major_id = major_options[major]
    date = st.date_input("日期", min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False
    is_fail = False

    with col1:
        if st.button("修改", type="primary"):
            if(majorchanges.change_major(
                student_id = student['StudentID'],
                new_major_id = major_id,
                change_date = str(date),
                db = st.session_state.db_connection
            )):
                is_success = True
            else:
                is_fail = True

    with col2:
        if st.button("取消"):
            st.rerun()

    if is_success:
        st.success("成功修改专业")
    if is_fail:
        st.error("修改专业失败")
    
@st.experimental_dialog("上传照片")
def upload_photo_dialog(student):
    st.write("上传照片")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    st.text_input("学号", value=student['StudentID'], disabled=True)
    uploaded_file = st.file_uploader("选择照片", type=['jpg', 'jpeg', 'png'])
    
    is_success = False
    is_fail = False
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        if students.upload_image(student['StudentID'], bytes_data, st.session_state.db_connection):
            is_success = True
        else:
            is_fail = True

    if is_success:
        st.success("上传成功")
    if is_fail:
        st.error("上传失败")

@st.experimental_dialog("查看照片")
def show_photo_dialog(student):
    st.write("学号为", student['StudentID'], "的学生照片")
    image = students.get_student_image(student['StudentID'], st.session_state.db_connection)
    if image is not None:
        st.image(image, caption="学生照片", use_column_width=True)
    else:
        st.write("该学生没有照片")

def show():
    frontend.utils.show_sidebar()
    st.title('学生信息管理')
    df = students.get_all_students(st.session_state.db_connection)

    selected = pd.DataFrame()
    if df.empty:
        st.write("数据库中没有学生信息")
    else:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination()
        gb.configure_side_bar()
        gb.configure_selection('single')
        gb.configure_grid_options(domLayout='normal', editable=False)
        grid_options = gb.build()

        response = AgGrid(
            df,
            gridOptions=grid_options,
            height=600,
            width='100%',
            update_mode=GridUpdateMode.SELECTION_CHANGED
        )

        selected = response['selected_rows']
        if selected is None:
            selected = pd.DataFrame()

    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("修改学生信息"):
            if not selected.empty:
                edit_student_dialog(selected.iloc[0])
            else:
                st.error("请选择一个学生")

        if st.button("查看学生奖惩信息"):
            if not selected.empty:
                show_student_rewards_punishments(selected.iloc[0])
            else:
                st.error("请选择一个学生")
        
        if st.button("修改专业信息"):
            if not selected.empty:
                edit_major_dialog(selected.iloc[0])
            else:
                st.error("请选择一个学生")
        
    
    with col2:
        if st.button("添加学生"):
            add_student_dialog()

        if st.button("添加奖惩信息"):
            if not selected.empty:
                add_award_punishment_dialog(selected.iloc[0])
            else:
                st.error("请选择一个学生")        
        
        if st.button("上传照片"):
            if not selected.empty:
                upload_photo_dialog(selected.iloc[0])
            else:
                st.error("请选择一个学生")
    
    with col3:
        if st.button("删除学生"):
            if not selected.empty:
                delete_student_dialog(selected.iloc[0])
            else:
                st.error("请选择一个学生")
        
        if st.button("查看学生选课信息"):
            if not selected.empty:
                show_student_enrollments(selected.iloc[0])
            else:
                st.error("请选择一个学生")
        
        if st.button("查看照片"):
            if not selected.empty:
                show_photo_dialog(selected.iloc[0])
            else:
                st.error("请选择一个学生")
    
    with col4:
        if st.button("刷新"):
            st.rerun()
        
        if st.button("添加选课信息"):
            if not selected.empty:
                add_enrollment_dialog(selected.iloc[0])
            else:
                st.error("请选择一个学生")
        
    # 检测是否需要刷新数据
    # if 'refresh' in st.session_state and st.session_state['refresh']:
    #     st.rerun()
    #     st.session_state['refresh'] = False

    
            
show()
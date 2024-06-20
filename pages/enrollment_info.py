from database import enrollments
import frontend.utils
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
import datetime

@st.experimental_dialog("添加选课信息")
def add_enrollment_dialog():
    st.write("添加选课信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    student_id = st.text_input("学号")
    course_id = st.text_input("课程ID")
    semester = st.selectbox("学期", ["2020秋季", "2021春季", "2021秋季", "2022春季", "2022秋季", "2023春季", "2023秋季", "2024春季", "2024秋季", "2025春季", "2025秋季"])

    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(enrollments.add_enrollment(
                student_id=student_id,
                course_id=int(course_id),
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
    elif is_fail:
        st.error("添加失败")

@st.experimental_dialog("删除选课信息")
def delete_enrollment_dialog(enrollment):
    st.write("删除选课信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("删除", type="primary"):
            if(enrollments.delete_enrollment(
                enrollment_id=enrollment['EnrollmentID'],
                db=st.session_state.db_connection
            )):
                is_success = True
            else:
                is_fail = True
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("删除成功")
    elif is_fail:
        st.error("删除失败")

@st.experimental_dialog("添加成绩")
def add_grade_dialog(enrollment):
    st.write("添加成绩")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    grade = st.number_input("成绩", min_value=0, max_value=100, step=1)

    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(enrollments.update_enrollment_grade(
                enrollment_id=enrollment['EnrollmentID'],
                grade=grade,
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
    elif is_fail:
        st.error("添加失败")

def show():
    frontend.utils.show_sidebar()
    st.title("选课信息")
    df = enrollments.get_all_enrollments(st.session_state.db_connection)

    if df.empty:
        st.write("没有选课信息")
    else:
        print(df)
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination()
        gb.configure_side_bar()
        gb.configure_selection('single')
        gb.configure_grid_options(domLayout='normal', editable=False)
        grid_options = gb.build()

        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            height=600,
            width='100%',
            update_mode=GridUpdateMode.SELECTION_CHANGED
        )

        selected = grid_response['selected_rows']
        if selected is None:
            selected = pd.DataFrame()
    
    col1, col2, col3, col4= st.columns([1, 1, 1, 1])
    with col1:
        if st.button("添加选课信息"):
            add_enrollment_dialog()
    
    with col2:
        if st.button("删除选课信息"):
            if not selected.empty:
                delete_enrollment_dialog(selected.iloc[0])
            else :
                st.error("请选择一个选课信息")

    with col3:
        if st.button("添加成绩"):
            if not selected.empty:
                add_grade_dialog(selected.iloc[0])
            else :
                st.error("请选择一个选课信息")

    with col4:
        if st.button("刷新"):
            st.rerun()

show()

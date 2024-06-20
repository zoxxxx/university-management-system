from database import courses, colleges
import frontend.utils
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
import datetime

@st.experimental_dialog("添加课程信息")
def add_course_dialog():
    st.write("添加课程信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    course_name = st.text_input("课程名称")
    credits = st.number_input("学分", min_value=1.0, max_value=10.0, step=0.5)

    colleges_df = colleges.get_all_colleges(st.session_state.db_connection)
    college_options = dict(zip(colleges_df['CollegeName'], colleges_df['CollegeID']))
    selected_college_name = st.selectbox("开课学院", list(college_options.keys()))
    offering_college_id = college_options[selected_college_name]

    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(courses.add_course(
                course_name=course_name,
                credits=credits,
                offering_college_id=offering_college_id,
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

@st.experimental_dialog("删除课程信息")
def delete_course_dialog(course):
    st.write("删除课程信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("删除", type="primary"):
            if(courses.delete_course(
                course_id=course['CourseID'],
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

def show():
    frontend.utils.show_sidebar()
    st.title("课程信息")
    df = courses.get_all_courses(st.session_state.db_connection)

    if df.empty:
        st.write("没有课程信息")
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
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("添加课程信息"):
            add_course_dialog()
    
    with col2:
        if st.button("删除课程信息"):
            if not selected.empty:
                delete_course_dialog(selected.iloc[0])
            else :
                st.error("请选择一个课程信息")

    with col3:
        if st.button("刷新"):
            st.rerun()

show()


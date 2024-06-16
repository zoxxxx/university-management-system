from database import majors, colleges
import frontend.utils
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd

@st.experimental_dialog("添加专业信息")
def add_major_dialog():
    st.write("添加专业信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    major_name = st.text_input("专业名称")
    
    # 获取所有学院的数据
    colleges_df = colleges.get_all_colleges(st.session_state.db_connection)
    college_options = dict(zip(colleges_df['CollegeName'], colleges_df['CollegeID']))
    selected_college_name = st.selectbox("所属学院", list(college_options.keys()))
    college_id = college_options[selected_college_name]

    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(majors.add_major(major_name, college_id, st.session_state.db_connection)):
                is_success = True
            else:
                is_fail = True
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("专业添加成功")
    elif is_fail:
        st.error("添加失败，请检查输入或数据库连接")

@st.experimental_dialog("删除专业信息")
def delete_major_dialog(major):
    st.write("删除专业信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("删除", type="primary"):
            if(majors.delete_major(major['MajorID'], st.session_state.db_connection)):
                is_success = True
            else:
                is_fail = True
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("专业删除成功")
    elif is_fail:
        st.error("删除失败，请检查专业ID或数据库连接")

def show():
    frontend.utils.show_sidebar()
    st.title("专业信息管理")
    df = majors.get_all_majors(st.session_state.db_connection)

    if df.empty:
        st.write("没有专业信息")
    else:
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
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("添加专业信息"):
            add_major_dialog()
    
    with col2:
        if st.button("删除专业信息") and selected:
            delete_major_dialog(selected.iloc[0])

    with col3:
        if st.button("刷新"):
            st.rerun()

show()

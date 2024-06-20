from database import colleges
import frontend.utils
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd

@st.experimental_dialog("添加学院信息")
def add_college_dialog():
    st.write("添加学院信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    college_name = st.text_input("学院名称")
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(colleges.add_college(college_name, st.session_state.db_connection)):
                is_success = True
            else:
                is_fail = True
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("学院添加成功")
    elif is_fail:
        st.error("添加失败")

@st.experimental_dialog("删除学院信息")
def delete_college_dialog(college):
    st.write("删除学院信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("删除", type="primary"):
            if(colleges.delete_college(college['CollegeID'], st.session_state.db_connection)):
                is_success = True
            else:
                is_fail = True
    
    with col2:
        if st.button("取消"):
            st.rerun()
    
    if is_success:
        st.success("学院删除成功")
    elif is_fail:
        st.error("删除失败")

def show():
    frontend.utils.show_sidebar()
    st.title("学院信息管理")
    df = colleges.get_all_colleges(st.session_state.db_connection)

    if df.empty:
        st.write("没有学院信息")
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
        if selected is None:
            selected = pd.DataFrame()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("添加学院信息"):
            add_college_dialog()
    
    with col2:
        if st.button("删除学院信息"):
            if selected.empty:
                st.error("请选择一个学院")
            else: 
                delete_college_dialog(selected.iloc[0])

    with col3:
        if st.button("刷新"):
            st.rerun()

show()

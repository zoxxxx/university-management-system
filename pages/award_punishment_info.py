from database import students, awards_punishments
import frontend.utils
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
import datetime

@st.experimental_dialog("添加奖惩信息")
def add_award_punishment_dialog():
    st.write("添加奖惩信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    student_id = st.text_input("学号")
    award_punishment = st.selectbox("奖惩", ["奖", "惩"])
    award_punishment_date = st.date_input("奖惩日期", min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    award_punishment_reason = st.text_input("奖惩原因")
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("添加", type="primary"):
            if(awards_punishments.add_award_punishment(
                student_id=student_id,
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
    elif is_fail:
        st.error("添加失败")

@st.experimental_dialog("删除奖惩信息")
def delete_award_punishment_dialog(award_punishment):
    st.write("删除奖惩信息")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    col1, _, col2 = st.columns([1, 1, 1])

    is_success = False  
    is_fail = False

    with col1:
        if st.button("删除", type="primary"):
            if(awards_punishments.delete_award_punishment(
                apid=award_punishment['APID'],
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
    st.title("奖惩信息")
    df = awards_punishments.get_all_awards_punishments(st.session_state.db_connection)

    if df.empty:
        st.write("没有奖惩信息")
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
        if st.button("添加奖惩信息"):
            add_award_punishment_dialog()
    
    with col2:
        if st.button("删除奖惩信息"):
            if selected.empty:
                st.error("请先选择一项")
            else:
                delete_award_punishment_dialog(selected.iloc[0])

    with col3:
        if st.button("刷新"):
            st.rerun()

show()
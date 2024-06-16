from database import students, awards_punishments
import frontend.utils
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
import datetime

def show():
    frontend.utils.show_sidebar()
    st.title("奖惩信息")
    df = awards_punishments.get_student_awards_punishments(student_id = st.session_state.student_id, db=st.session_state.db_connection)

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

    if st.button("刷新"):
        st.rerun()

show()
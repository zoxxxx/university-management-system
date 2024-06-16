import streamlit as st
from database import majorchanges
import frontend.utils
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd

def show():
    frontend.utils.show_sidebar()
    st.title("专业变更信息管理")
    # df = majors.get_(st.session_state.db_connection)
    df = majorchanges.get_all_majorchanges(st.session_state.db_connection)

    if df.empty:
        st.write("没有专业变更信息")
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
    
    if st.button("刷新"):
        st.rerun()

show()
import frontend
import database
import frontend.home
import streamlit as st
def main() -> None:
    st.set_option("client.showSidebarNavigation", False)
    if "db_connection" not in st.session_state or st.session_state.db_connection is None:
        st.session_state.db_connection = database.utils.create_db_connection()
    
    frontend.home.show()

if __name__ == "__main__":
    main()
import streamlit as st
import database.utils
import frontend
import frontend.login
import frontend.utils

def show():
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        frontend.utils.show_sidebar()

    else:
        if 'show_register' in st.session_state and st.session_state.show_register:
            frontend.login.register()
        else:
            frontend.login.login()


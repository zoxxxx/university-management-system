import streamlit as st
import frontend.login
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
import streamlit_antd_components as sac


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def show_admin_sidebar():
    with st.sidebar:
        st.title("导航")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            
            st.page_link("pages/student_info.py", label="学生信息管理", icon="🧑‍🎓")
            st.page_link("pages/award_punishment_info.py", label="奖惩信息管理", icon="🏅")
            st.page_link("pages/enrollment_info.py", label="选课信息管理", icon="📚")
            st.page_link("pages/course_info.py", label="课程信息管理", icon="📖")
            st.page_link("pages/college_info.py", label="学院信息管理", icon="🏫")
            st.page_link("pages/major_info.py", label="专业信息管理", icon="🎓")
            st.page_link("pages/majorchange_info.py", label="专业变更管理", icon="🔄")
            if st.button("登出", type="primary"):
                frontend.login.logout()

        elif get_current_page_name() != "main":
            st.switch_page("main.py")

def show_student_sidebar():
    with st.sidebar:
        st.title("导航")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/my_info.py", label="我的信息", icon="🧑‍🎓")
            st.page_link("pages/my_enrollment.py", label="我的选课", icon="📚")
            st.page_link("pages/my_award_punishment.py", label="我的奖惩", icon="🏅")
            
            st.write("")
            st.write("")

            if st.button("登出", type="primary"):
                frontend.login.logout()

        elif get_current_page_name() != "main":
            st.switch_page("main.py")

def show_sidebar():
    with st.sidebar:
        st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
        if st.session_state.get("logged_in", False):
            if st.session_state.get("role") == "admin":
                show_admin_sidebar()
            else:
                show_student_sidebar()

        elif get_current_page_name() != "main":
            st.switch_page("main.py")


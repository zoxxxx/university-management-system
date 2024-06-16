
import database.account
import database.utils
import streamlit as st
import streamlit_antd_components as sac
import hashlib

def authenticate(username, hashed_password, auto_login=False):
    db_connection = st.session_state.db_connection
    if db_connection is None:
        st.error("No database connection found.")
        return False

    if auto_login or database.account.verify_user(username, hashed_password, db_connection):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.session_state['role'] = database.account.get_user_role(username, db_connection) 
        if st.session_state['role'] == "student":
            st.session_state['student_id'] = database.account.get_student_id(username, db_connection)
        return True
    else:
        return False

def register():
    db_connection = st.session_state.db_connection
    st.subheader("注册新账户")
    username = st.text_input("用户名", placeholder="请输入用户名")
    password = st.text_input("密码", type="password", placeholder="请输入密码")
    check_password = st.text_input("确认密码", type="password", placeholder="请确认密码")
    student_id = st.text_input("学号", placeholder="请输入学号")
    
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    
    _, col1, col2, _ = st.columns([1, 1, 1, 1])
    register_pressed = False
    with col1:
        if st.button("注册", type="primary"):
            register_pressed = True

    with col2:
        if st.button("返回登录", type="secondary"):
            st.session_state['show_register'] = False
            st.rerun()

    if register_pressed:
        if password != check_password:
            st.error("两次输入的密码不一致")
        elif not all([username, password, student_id]):
            st.error("所有字段均为必填项")
        else:
            hashed_password = hashlib.sha512(password.encode()).hexdigest()
            if database.account.create_user(username, hashed_password, "student", db_connection, student_id):
                st.success("注册成功！自动登录中...")
                if authenticate(username, hashed_password, auto_login=True):
                    st.success("登录成功！")
                    st.rerun()
            else:
                st.error("注册失败，请检查重试或联系管理员。")

def login():
    st.subheader("用户登录")
    username = st.text_input("用户名", placeholder="请输入用户名")
    password = st.text_input("密码", type="password", placeholder="请输入密码")
    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)

    _, col1, col2, _ = st.columns([1, 1, 1, 1])
    login_pressed = False
    with col1:
        if st.button("登录", type="primary"):
            login_pressed = True

    with col2:
        if st.button("注册新账户", type="secondary"):
            st.session_state['show_register'] = True
            st.rerun()

    if login_pressed:
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        if authenticate(username, hashed_password):
            st.success("登录成功！")
            st.rerun()
        else:
            st.error("用户名或密码错误")

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    st.switch_page("main.py")
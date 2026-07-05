import streamlit as st
st.set_page_config(
    page_title="AI伴侣",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)
#大标题
st.title("AI伴侣")
st.write("欢迎来到AI伴侣")

prompt=st.chat_input("请输入你的问题")
if prompt:
    st.write(f"用户:{prompt}")

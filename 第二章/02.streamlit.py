import streamlit as st

st.set_page_config(
    page_title="Streamlit 入门",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Streamlit")
st.header("Streamlit一级标题")
st.subheader("Streamlit二级标题")
#段落文字
st.write("哈哈，那我来给你讲一个关于科学的笑话吧！\n\n为什么物理学家和生物学家的恋爱总是很复杂？\n\n—— 因为物理学家总想搞清everything（一切的原理），而生物学家只关注living things（生活的琐事），两个人最后发现，最大的共同点就是——他们都活在“压力”下！\n\n一个中子走进一家酒吧，要了一杯啤酒。\n“多少钱？”中子问。\n酒保微笑着回答：“对你嘛，免费！”\n中子惊喜地问：“为什么？”\n酒保耸耸肩：“因为你没有charge（电荷/账单）啊！”\n\n哈哈，是不是有点“冷”？科学就是可以这么幽默～😄\n\n想挑战更多脑洞，随时找我哦！")
#图片
st.image("./resources/光盘行动.jpg",width=100)
# #音频
# st.audio("")
# #视频
# st.video("")
# #logo
# st.logo("")
#表格
student_data = {
    "姓名":["鳄鱼","李凡","石浩","唐三"],
    "语文":["鳄鱼","李凡","石浩","唐三"],
    "英语":["鳄鱼","李凡","石浩","唐三"],
    "数学":["鳄鱼","李凡","石浩","唐三"]
}
st.table(student_data)

#输入框
name=st.text_input("输入姓名:")
st.write("输入的姓名为：",name)
password=st.text_input("输入姓名:",type="password")
st.write("输入的姓名为：",password)
#单选按钮
gender=st.radio("输入性别：",["male","female","other"],index=2)
st.write("性别为：",gender)
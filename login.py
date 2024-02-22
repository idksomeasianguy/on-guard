import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
   page_title="Login - On Guard",
   page_icon="🤺"
)

st.title(":fencer: On Guard")
st.subheader("Log In")
with st.form(key="login", clear_on_submit=True):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.form_submit_button("Log In")
    if login:
        if username != "TeamVCIS":
            st.error("Wrong username!")
        
        if password != "victory":
            st.error("Wrong password!")
        
        if username == "TeamVCIS" and password == "victory":
            switch_page("monitor")

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://cdn.discordapp.com/attachments/1148881767957270538/1210114620019187712/Gradient_Blue_Background.jpg?ex=65e96210&is=65d6ed10&hm=0b9e2039117f4cf088cc5afabb93366f7815af98dfacf93972f0db3c9e76d93a&");
  background-size: cover;
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)
import streamlit as st

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://cdn.discordapp.com/attachments/1148881767957270538/1210114620019187712/Gradient_Blue_Background.jpg?ex=65e96210&is=65d6ed10&hm=0b9e2039117f4cf088cc5afabb93366f7815af98dfacf93972f0db3c9e76d93a&");
  background-size: cover;
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

st.title('On Guard')
st.subheader('We believe that the youth is the hope of the nation and we would like to be part of the solution.')

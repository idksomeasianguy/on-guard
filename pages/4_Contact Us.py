import streamlit as st
from PIL import Image

st.set_page_config(
   page_title="Contact Us - On Guard",
)

logo = Image.open("on_guard_logo.jpg")
st.image(logo, width=400)

st.title('Contact Us')

st.subheader('You can reach out to us if you have any questions through email or social media!')
st.subheader('Email: onguard.vcis@gmail.com')

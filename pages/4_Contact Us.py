import streamlit as st
from PIL import Image

st.set_page_config(
   page_title="Contact Us - On Guard",
)

logo = Image.open("on_guard_logo.jpg")
st.image(logo, width=400)


st.title('Contact Us')


Concerns = '<p style="font-size: 20px;">Feel free to reach out to us if you have any questions or concerns through our email, contact number, or social media platforms!</p>'
st.markdown(Concerns, unsafe_allow_html=True)

st.subheader('Email: onguard.vcis@gmail.com')
st.subheader('Contact Number: +63 101 234 5678')


st.subheader('Social Media Platforms')
socmed = '<p style="font-size: 20px;">Facebook: On Guard</p>'
st.markdown(socmed, unsafe_allow_html=True)
Instagram = '<p style="font-size: 20px;">Instagram: On Guard</p>'
st.markdown(Instagram, unsafe_allow_html=True)

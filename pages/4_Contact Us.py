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

col1, mid, col2 = st.columns([1,1,20])
with col1:
    on = Image.open('Facebook-Logo.png')
    st.image(on, width=80)
with col2:
    s = f"<p style='font-size:20px;'>{'On Guard'}</p>"
    st.markdown(s, unsafe_allow_html=True) 

side, col1, mid, col2 = st.columns([0.5,1,0.5,20])
with col1:
    on = Image.open('Insta.png')
    st.image(on, width=45)
with col2:
    s = f"<p style='font-size:20px;'>{'On Guard'}</p>"
    st.markdown(s, unsafe_allow_html=True) 

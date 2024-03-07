import streamlit as st
from PIL import Image


st.set_page_config(
   page_title="Home - On Guard",
)

logo = Image.open("on_guard_logo.jpg")
st.image(logo, width=400)


video_file = open('Guide.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

st.subheader('We believe that the youth is the hope of the nation and we would like to be part of the solution.')

st.markdown("The youth are at risk of exposure to inappropriate content, leaking sensitive information, talking to strangers with malicious intentions, and being too dependent on social media. Researchers also shared that young individuals under 25 years old who are victims of cyber bullying are prone to self-harm and suicidal behaviors and another study revealed that due to gadgets’ excessive use, it could lead to emotional problems, familial conflicts and pushing people towards self isolation.")

st.markdown("The solution? On Guard! On Guard is a message content monitoring app created to assist parents and guardians to be a digital protector of their children in the online world. We aim to keep every Filipino child safe from the potential threats online.")

st.markdown("On Guard monitors conversations from online platforms to identify which is safe and which contains potential threats such as cyberbullying, explicit content, and online predators. It also detects over 133 different languages entered in our text and screenshot detector. The kids' conversations will remain private. Parents will only receive notifications when threats are detected.")

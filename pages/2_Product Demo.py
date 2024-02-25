import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from googletrans import Translator
import smtplib
from email.mime.text import MIMEText
import re
import easyocr as ocr
from PIL import Image
import vonage
import whisper
from tempfile import NamedTemporaryFile

st.set_page_config(
   page_title="Product Demo - On Guard",
)
st.markdown("""<style>
               div.stButton > button:first-child {
                  background-color: white;
                  color: #64A8E7;
               } 
               div.stButton > button:first-child:hover {
                  background-color: #64A8E7;
                  color: white;
               }
               </style>""", unsafe_allow_html=True)

@st.cache_data(show_spinner="Loading data...")
def load_data():
   df = pd.read_csv("Phishing_Email.csv")
   e = pd.DataFrame({
      "Unnamed: 0": [18651, 18652],
      "Email Text": ["carb23 02/11/2024 9.04 PM You're such a loser Freakl You dont deserve to be in our class Everyone in school hates you", "Hello bunso How are you bunso? It's been a while I'm doing good kuya yeah it's really been a while"],
      "Email Type": ["Phishing Email", "Safe Email"]
   })
   df = df._append(e, ignore_index=True)
   return df

@st.cache_resource(show_spinner="Loading the image reader...")
def load_reader():
   reader = ocr.Reader(["en"], model_storage_directory=".")
   return reader

@st.cache_resource(show_spinner="Loading Whisper...")
def load_whisper():
   w = whisper.load_model("base")
   return w

logo = Image.open("on_guard_logo.jpg")
st.image(logo, width=400)

with st.form(key="my_form", clear_on_submit=True):
   text = st.text_area("Text to analyze")
   images = st.file_uploader(label="Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
   raw_audio = st.file_uploader(label="Upload audio", type=["mp3", "mp4", "wav", "aac", "m4a"], accept_multiple_files=True, key="audio")
   user_email = st.text_input("(Recommended) Send alerts to:", placeholder="juandelacruz@gmail.com")
   phone_number = st.text_input("(Recommended) Send SMS notifications to:", placeholder="+63 999 999 9999")
   submit_button = st.form_submit_button(label="Monitor my child's conversations!")

raw_spam_data = load_data()
spam_data = raw_spam_data.where((pd.notnull(raw_spam_data)),"")
spam_data.loc[spam_data["Email Type"] == 'Phishing Email', "Email Type",] = 1
spam_data.loc[spam_data["Email Type"] == 'Safe Email', "Email Type",] = 0

X = spam_data["Email Text"]
y = spam_data["Email Type"]

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=1)

feature_extraction = TfidfVectorizer(min_df=1, stop_words='english')

X_train_features = feature_extraction.fit_transform(X_train)
X_test_features = feature_extraction.transform(X_val)

y_train = y_train.astype('int')
y_test = y_val.astype('int')
model = LogisticRegression()
model.fit(X_train_features, y_train)

def detect(text):
   text = [text]
   input_data_features = feature_extraction.transform(text)
   prediction = model.predict(input_data_features)
   keywords = ["kys", "loser", "freak", "kill yourself"]
   if any([x in keywords for x in text[0].split()]):
      prediction = [1]
   return prediction

notif_text = []
translator = Translator()
reader = load_reader()
client = vonage.Client(key=st.secrets["key"], secret=st.secrets["secret"])
file_results = []

if submit_button:
   with st.spinner("Processing your input..."):
      if len(text) == 0 or text.isspace():
         st.write("The provided text is empty!")
      else:
         text = translator.translate(text).text
         if detect(text)[0] == 1:
            st.write(":red[:triangular_flag_on_post: Threat detected in the provided text!]")
            notif_text.append("Threat detected in the provided text!")
            notif_text.append(text)
            notif_text.append("\n")
         else:
            st.write(":green[:thumbsup: Looks like the provided text is safe!]")

      if len(images) > 0:
         for img in images:
            input_image = Image.open(img)
            result = reader.readtext(np.array(input_image))
            img_text = []

            for text in result:
               img_text.append(text[1])
            
            if len(img_text) == 0:
               st.write(f"We couldn't see any text in {img.name}.")
            else:
               img_content = " ".join(img_text)
               img_content = translator.translate(img_content).text
               if detect(img_content)[0] == 1:
                  st.write(f":red[:triangular_flag_on_post: Threat detected in {img.name}!]")
                  notif_text.append(f"Threat detected in {img.name}!")
                  notif_text.append(img_content)
                  notif_text.append("\n")
               else:
                  st.write(f":green[:thumbsup: Looks like {img.name} is safe!]")
      if len(raw_audio) > 0:
         for a in raw_audio:
               with NamedTemporaryFile(suffix="mp3") as temp:
                  temp.write(a.getvalue())
                  temp.seek(0)
                  whisper_model = whisper.load_model("base")
                  result = whisper_model.transcribe(temp.name)
                  audio_content = str(result["text"])
                  audio_content = translator.translate(audio_content).text
                  if detect(audio_content)[0] == 1:
                     file_results.append(f":red[:triangular_flag_on_post: Threat detected in {a.name}!]")
                     notif_text.append(f"Threat detected in {a.name}!")
                     notif_text.append(audio_content)
                     notif_text.append("\n")
                  else:
                     file_results.append(f":green[:thumbsup: Looks like {a.name} is safe!]")

   email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
   if re.fullmatch(email_pattern, user_email):
      notif_text = "\n".join(notif_text)
      msg = MIMEText(notif_text)
      msg["From"] = st.secrets["email"]
      msg["To"] = user_email
      msg["Subject"] = "Results from On Guard's text analysis"
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(st.secrets["email"], st.secrets["password"])
      server.sendmail(st.secrets["email"], user_email, msg.as_string())
      server.quit()
   
   phone_pattern = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
   if re.fullmatch(phone_pattern, phone_number):
      if type(notif_text) is list:
         notif_text = "\n".join(notif_text)
      phone_number = "".join(phone_number.split())
      response = client.sms.send_message(
         {
            "from": "On Guard",
            "to": phone_number,
            "text": notif_text,
         }
      )

   if len(notif_text) > 0 and re.fullmatch(email_pattern, user_email) and re.fullmatch(phone_pattern, phone_number):
      st.error("There was a threat in your provided file(s)! More details will be sent through your email and/or SMS. If you don't see it, check your spam.", icon="🚩")
   elif len(images) > 0 and len(raw_audio) > 0 and len(notif_text) == 0:
      st.success("Good news! Looks like all of your files are safe!", icon="👍")
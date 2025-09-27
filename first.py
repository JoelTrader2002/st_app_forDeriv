import streamlit as st
import smtplib
from email.mime.text import MIMEText

# displaying text

st.title("my title")

st.header("this is my header",divider="gray")

st.subheader("this is subheader")

st.markdown("**am good**")

st.html('<h1 style="color: aqua; " >am good</h1>')


tab1,tab2=st.tabs(tabs=['        tab1         ','        tab2      '])

tab1.title("am good")

tab2.title("am good perfect")





#email parameter 
sender_email="joelndabila2002@gmail.com"
receiver_email="joelezekia1234@gmail.com"
password="nxtg bywk gjhn hogm"
subject="subject"
body="my email sent"

# create a text massage

msg=MIMEText(body)
msg['Subject']=subject
msg['From']=sender_email
msg['To']=receiver_email

#set up smtp server

server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(user=sender_email,password=password)

#send email

server.sendmail(sender_email,receiver_email,msg.as_string())
server.quit()

st.rerun()


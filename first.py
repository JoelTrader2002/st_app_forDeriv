import streamlit as st
import smtplib
from email.mime.text import MIMEText
import asyncio
import websockets
import json
import websocket
# displaying text


#deriv cresidential
deriv_api_token=st.secrets["deriv_api"]["api"]
deriv_app_id=st.secrets["deriv_app_id"]["app"]
deriv_url=f"wss://ws.derivws.com/websockets/v3?app_id={deriv_app_id}"

#authorize
authorize={
    "authorize":deriv_api_token
          }



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
body="my email sent first .py "

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





web=websocket.WebSocket()


web.connect(deriv_url)


#authorize connection
authorization={
    "authorize":deriv_api_token
}

web.send(json.dumps(authorization))
response=json.loads(web.recv())

if response.get("error")==None:
    print(response)
else:
    print(response.get("error"))  






proposal_r = {
            'proposal': 1,
            'amount': 1,  # Stake $10
            'basis': 'stake',  # Stake-based contract
            'contract_type': 'ONETOUCH',  # Predict price goes up
            'currency': 'USD',
            'duration': 15,  # 15 minutes
            'duration_unit': 'm',  # Minutes (common for forex)
            'symbol':'R_50',  # EUR/USD forex pair
            'req_id': 2,
            "barrier":"+10"
        }



web.send(json.dumps(proposal_r))

response=json.loads(web.recv())

if response.get("error")==None:
    print('propposal for eurusd')
    print(response['proposal'])
else:
    print(response.get("error"))    




proposal_id = response['proposal']['id']
ask_price = response['proposal']['ask_price']
        # Step: Buy the contract
buy_msg = {
            'buy': proposal_id,
            'price': ask_price,
            'req_id': 3
        }


print(buy_msg)

web.send(json.dumps(buy_msg))

response=json.loads(web.recv())


print("")
print("")
if response.get("error")==None:
    print(response)
else:
    print(response.get("error"))    


open_pos={
        'proposal_open_contract': 1,
            'subscribe': 1,  # Real-time updates for profit/loss
            'req_id': 2
}

web.send(json.dumps(open_pos))

res=json.loads(web.recv())


print(res)






web.close()







st.rerun()


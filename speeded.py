import streamlit as st
import pandas as pd
import plotly as plot
from plotly import graph_objects as go
import json
import io
import websockets
import asyncio
from technical_analysis import indicators as indicator
from ta import momentum,trend,volatility
from streamlit_navigation_bar import st_navbar
import smtplib
from email.mime.text import MIMEText

#deriv cresidential
deriv_api_token=st.secrets["deriv_api"]["api"]
deriv_app_id=st.secrets["deriv_app_id"]["app"]
deriv_url=f"wss://ws.derivws.com/websockets/v3?app_id={deriv_app_id}"

#authorize
authorize={
    "authorize":deriv_api_token
          }

profit_table={
   "profit_table":1,
   "description":1,
   "limit":25,
   "offset":25,
   "sort":"ASC"
}

open_contracts_list={
        'proposal_open_contract': 1,
            'subscribe': 1,  # Real-time updates for profit/loss
            'req_id': 2
}

statement={
   "statement":1,
   "description":1,
   "limit":999,
}

balance_req={
   "balance":1,
   "subscribe":1
}





async def auth(req):
    async with websockets.connect(deriv_url) as web:
        # Authorize
        await web.send(json.dumps(authorize))
        autho = json.loads(await web.recv())

        # Profit Table
        await web.send(json.dumps(req))
        respo = json.loads(await web.recv())

        # Open Contracts

        # Collect responses

    return respo



async def main_func():
   tasks=[auth(req=profit_table),auth(req=open_contracts_list),auth(req=statement),auth(req=balance_req)]
   data=await asyncio.gather(*tasks)
   return data



# Run the async function inside Streamlit
data = asyncio.run(main_func())



# Sample data (from provided code)
balance =data[3]['balance']['balance']
name = "JOEL EZEKIA NDABILA"
email = "joelndabila2002@gmail.com"

history_pos=data[0]['profit_table']['transactions']

account_statement=data[2]

history = []   # list instead of dict

for pos in history_pos:   # history_pos is your JSON transactions
    symbol = pos['underlying_symbol']
    stake = pos['buy_price']
    ret = pos['sell_price']
    profit = ret - stake

    history.append({
        "symbol": symbol,
        "stake": stake,
        "profit": profit
    })

# Convert to DataFrame
df_history = pd.DataFrame(history)


open_pos = data[1]  # Example: Could be list of dicts like [{'Trade ID': 1, 'Asset': 'EUR/USD', 'Type': 'Call', 'Amount': 100, 'Expiry': '10 min'}]




st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# ---- Custom CSS for styling ----

st.title("deriv binary trading")
st.html("<br> </br>")
cola,colb=st.columns([2,1])
with cola:
      st.subheader(f"{name}")
      st.subheader(f"{email}")

with colb:
      st.header(f"${balance:.3f}")

colA,colB=st.columns(2)


# Open Positions Section
with colA:
 st.subheader("open position")
 if open_pos:
    open_df = pd.DataFrame(open_pos)  # Convert to DataFrame for table display
    st.dataframe(open_df, use_container_width=True)
 else:
    st.info("No open positions currently.")

# Closed Positions Section
with colB:
 st.subheader("position history")
 if history_pos:
      # Convert to DataFrame for table display
    st.dataframe(df_history, use_container_width=True)
 else:
    st.info("No closed positions yet.")



#account statement as dict

balance_history=[]
for trans in account_statement['statement']['transactions']:
   balance_history.append({"balance":trans['balance_after'],"time":trans['transaction_time']})

   
balance_history=pd.DataFrame(balance_history)

balance_history['time']=pd.to_datetime(balance_history['time'],unit='s')


balance_history=balance_history.sort_index(ascending=False)
balance_history['index']=range(len(balance_history))


balance_line_chart=go.Scatter(x=balance_history['index'],y=balance_history['balance'],)

figure=go.Figure(data=[balance_line_chart])

figure.update_layout(
   title="account balance",
   yaxis_range=[balance_history["balance"].min()-50,balance_history['balance'].max()+10]
)

st.plotly_chart(figure)

st.header("📈 deriv volatility index Analysis Dashboard")

    # ---- Top filters ----




my_symbols=['1HZ10V', 'R_10', '1HZ15V', '1HZ25V', 'R_25', '1HZ30V', '1HZ50V', 'R_50', '1HZ75V', 'R_75', '1HZ90V', '1HZ100V', 'R_100']
granularity=[60,180,300,900,1800,3600,7200]

historical_data={
   "ticks_history":"",
   "adjust_start_time":1,
   "count":500,
   "end":"latest",
   "style":"candles",
   "granularity":"",
}


async def fetch_data(req,granularity,symbol):
  async  with websockets.connect(deriv_url,open_timeout=30,ping_interval=30,ping_timeout=30,close_timeout=30) as web:
    req=historical_data.copy()
    req['granularity']=granularity
    req['ticks_history']=symbol

    await web.send(json.dumps(req))
    respo=await web.recv()
    respo=json.loads(respo)
    return respo


async def main():
   #create a list of task
   tasks=[]
   for symb in my_symbols:
    for granu in granularity:
      task=fetch_data(req=historical_data,granularity=granu,symbol=symb)
      tasks.append(task)  
   res=await asyncio.gather(*tasks)
   return res

res=asyncio.run(main=main())

st.write("data from fetch")
st.write(len(res))


def organize(data):
  mynewDict={}
  for item in data:
    symbol=item['echo_req']['ticks_history']
    timeframe=item['echo_req']['granularity']
    candles=pd.DataFrame(item.get("candles",{}))
    candles['time']=pd.to_datetime(candles['epoch'],unit='s')

    if symbol not in mynewDict:
      mynewDict[symbol]={}
    mynewDict[symbol][timeframe]=candles
  return mynewDict



organized_dict=organize(res)




data_inPandas=organized_dict['R_50'][300]

candlestick=go.Candlestick(
    x=data_inPandas['time'],
    open=data_inPandas['open'],
    close=data_inPandas['close'],
    high=data_inPandas['high'],
    low=data_inPandas['low'],
    increasing_line_color="#000000",
    decreasing_line_color="#000000",
    decreasing_fillcolor="#000000",
    increasing_fillcolor="#ffffff"
)

figures=go.Figure(data=[candlestick])
#remove a range slider which is an image boloew main image
figures.update_layout(xaxis_rangeslider_visible=False,
                     
                     paper_bgcolor='white',
                     plot_bgcolor='white',
                     yaxis=dict(autorange=True)
                     )

st.plotly_chart(figures)


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




proposal = {
            'proposal': 1,
            'amount': 1,  # Stake $10
            'basis': 'stake',  # Stake-based contract
            'contract_type': 'ONETOUCH',  # Predict price goes up
            'currency': 'USD',
            'duration': 15,  # 15 minutes
            'duration_unit': 'm',  # Minutes (common for forex)
            'symbol':'R_75',  # EUR/USD forex pair
            'req_id': 2,
            "barrier":"+20"
        }




async def send_proposal():
   async with websockets.connect(deriv_url) as web:
      web.send(json.dumps(authorize))
      web.recv()
      await web.send(json.dumps(proposal))

      response=await(web.recv())



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

      response=web.recv()


 

asyncio.run(main=send_proposal())




st.rerun()




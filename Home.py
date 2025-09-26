import streamlit as st
import pandas as pd
import plotly as plot
from plotly import graph_objects as go
import json
import io
import websocket
from streamlit_autorefresh import st_autorefresh




st.title("deriv binary trading")
















deriv_api_token=st.secrets["deriv_api"]["api"]
deriv_app_id=st.secrets["deriv_app_id"]["app"]
deriv_url=f"wss://ws.derivws.com/websockets/v3?app_id={deriv_app_id}"
# request to api



symbol_with_onetouch_contracts=['RDBEAR', 'RDBULL', '1HZ10V', 'R_10', '1HZ15V', '1HZ25V', 'R_25', '1HZ30V', '1HZ50V', 'R_50', '1HZ75V', 'R_75', '1HZ90V', '1HZ100V', 'R_100']
selected=symbol_with_onetouch_contracts[3]
contract_id=''
amount=""

historical_data={
   "ticks_history":selected,
   "adjust_start_time":1,
   "count":30,
   "end":"latest",
   "start":1,
   "style":"candles",
   "subscribe":1,
   "granularity":600,
   "req_id":1

}

proposal_for_oneTouch = {
            'proposal': 1,
            'amount': 1,  # Stake $10
            'basis': 'stake',  # Stake-based contract
            'contract_type': 'ONETOUCH',  # Predict price goes up
            'currency': 'USD',
            'duration': 15,  # 15 minutes
            'duration_unit': 'm',  # Minutes (common for forex)
            'symbol':'frxEURUSD',  # EUR/USD forex pair
            'req_id': 2,
            "barrier":"+12.3"
        }



# this require authorization

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

balance_request={
   "balance":1,
   "subscribe":1
}


open_contracts_list={
        'proposal_open_contract': 1,
            'subscribe': 1,  # Real-time updates for profit/loss
            'req_id': 2
}


open_contract={
   "buy":contract_id,
   "price":amount
}



#auto refresh the streamlite home.py app

#st_autorefresh(interval=5000,limit=None,key="counter")


name="jojooooo"
col1,col2=st.columns([2,1])




with st.container():
   st.header("row 1")
   st.write("am fine")
 


   with col2:
     st.button("col2")
     st.html(body="<h1> am joel </h1>")   

   with col1:
     st.button(label="col1")
     st.header("your good")
     st.write(f"account name {name}")








st.html("<h1>deriv binary trading</h1>")


#deriv cresidential


# connect to deriv
deriv_websocket=websocket.WebSocket()




#authorize

response=''

try:
    #connect to deriv api and authorize user
    deriv_websocket.connect(url=deriv_url)
    deriv_websocket.send(json.dumps(authorize))
except Exception as e:
    st.write(f"error during connecting, error massage {e}") 
else:
    response=json.loads(deriv_websocket.recv())
    if response.get("error")==None:
      st.write("successful connected")
      st.write(response['authorize']['fullname'])
    else:
      st.write("unable to connect to deriv url") 




try:   
  deriv_websocket.send(json.dumps(balance_request))
  account_balance=json.loads(deriv_websocket.recv())
except Exception as e:
   st.write("error reuesting balance, error massage {e}")
else:   
    st.write(f"your account balance is {account_balance['balance']['balance']} {account_balance['balance']['currency']}")




labels=['bear index','bull index','volatility 10s','volatility 10','volatility 15s','volatility 25s','volatility 25','volatility 30s','volatility 50s','volatility 50','volatility 75s','volatility 75','volatility 90s','volatility 100s','volatility 100']
st.write("select symbol to visualize data")
selected=st.selectbox(label="choose a pair",options=symbol_with_onetouch_contracts)
historical_data['ticks_history']=selected

try:
   deriv_websocket.send(json.dumps(historical_data))
except Exception as e:
   st.write(f"error during fetching histolocal data, error msg {e}")
else:
   data=json.loads(deriv_websocket.recv())
   st.dataframe(pd.DataFrame(data['candles']))      




def get_data_from_deriv(web,req):
   try:
      web.send(json.dumps(req))
      respo=json.loads(web.recv())
   except Exception as e:
      st.warning(e)
   else:
      return respo      
   





profit=get_data_from_deriv(deriv_websocket,req=profit_table)
open_pos=get_data_from_deriv(deriv_websocket,req=open_contracts_list)
historical_data['count']=100
historical_data['req_id']=2
data=get_data_from_deriv(web=deriv_websocket,req=historical_data)

st.write(profit)
st.write(open_pos)
st.write(data)





   
deriv_websocket.close()

#st.rerun()


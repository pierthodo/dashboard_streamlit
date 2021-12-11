import ccxt
import pandas as pd
import streamlit as st
import json
from pymongo import MongoClient
import plotly.express as px


from google.cloud import secretmanager



#balance = client.Account.balance
#df = pd.DataFrame([b for b in balance.find({"Id":"cryptellite"},{"Balance":1,"Time":1,"_id":0})])
#df["Time"] = df["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")

#fig = px.line(df, x='Time', y="Balance")
#st.plotly_chart(fig)


client = secretmanager.SecretManagerServiceClient()
name = f"projects/trading1/secrets/url-mongodb/versions/latest"
URL_MONGODB = client.access_secret_version(request={"name": name}).payload.data.decode("UTF-8")

client = MongoClient(URL_MONGODB)

signal = client.Signal.signal_trend_follow
df = pd.DataFrame([b for b in signal.find({"Strategy_name":"strat_1"},{"Signal":1,"Time":1,"_id":0})])
#df["Time"] = df["Time"].dt.strftime("%Y-%m-%d")

fig = px.line(df, x='Time', y="Signal")
st.plotly_chart(fig)



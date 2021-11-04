import ccxt
import pandas as pd
import streamlit as st
import json
from pymongo import MongoClient
import plotly.express as px


from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = f"projects/trading1/secrets/url-mongodb/versions/latest"
URL_MONGODB = client.access_secret_version(request={"name": name}).payload.data.decode("UTF-8")

client = MongoClient(URL_MONGODB)
## Plot value account cryptellite on binance
balance = client.Account.balance
df = pd.DataFrame([b for b in balance.find({"Id":"cryptellite"},{"Balance":1,"Time":1,"_id":0})])
df["Time"] = df["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")

fig = px.line(df, x='Time', y="Balance")
st.plotly_chart(fig)

# plot value account running the funding strategy on bybit

df = pd.DataFrame([b for b in balance.find({"Id":"bybit_funding"},{"Balance":1,"Time":1,"_id":0})])
df["Time"] = df["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")

fig = px.line(df, x='Time', y="Balance")
st.plotly_chart(fig)


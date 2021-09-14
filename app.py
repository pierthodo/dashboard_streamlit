import ccxt
import pandas as pd
import streamlit as st
import json
# Ftx keys
def standardize_postion(dic,exchange_name):
    #print(dic)
    if exchange_name == 'binance':
        side = "Buy" if float(dic['positionAmt']) > 0 else "Short"
        return {'symbol':dic["symbol"],
                'size':float(dic['positionAmt']),
                'side':side,
                'Pnl': float(dic['unrealizedProfit']),
                'notional': float(dic['notional']),
                'exchange':"binance"
        }
    elif exchange_name == 'ftx':
        price = exchange_ftx.fetch_ticker(dic["future"])["bid"]
        notional = float(dic["size"])*price
        return {'symbol':dic["future"],
                'size':float(dic['size']),
                'side':dic['side'],
                'notional':notional,
                'Pnl': float(dic['realizedPnl']),
                'exchange':'ftx'
        }


for s in ["","_FOLLOW"]:
    KEY = st.secrets["KEY_FTX"+s]
    SECRET = st.secrets["SECRET_FTX"+s]
    if s == "_FOLLOW":
        exchange_ftx = ccxt.ftx({'apiKey':KEY,'secret':SECRET,'headers': {
                'FTX-SUBACCOUNT': 'follownapbots',
            }
        })
    else:
        exchange_ftx = ccxt.ftx({'apiKey':KEY,'secret':SECRET,'headers': {
                'FTX-SUBACCOUNT': 'napbots',
            }
        })
    info = exchange_ftx.fetchBalance()
    balance_value = info['info']['result'][0]['total']
    print(balance_value)
    positions = exchange_ftx.fetch_account_positions()

    data = [standardize_postion(pos,'ftx') for pos in positions]
    # Binance keys
    KEY = st.secrets["KEY_BINANCE"+s]
    SECRET = st.secrets["SECRET_BINANCE"+s]
    exchange_binance = ccxt.binance({'apiKey':KEY,'secret':SECRET,'options': {'defaultType': 'future' }})

    info = exchange_binance.fetchBalance()
    positions = info['info']['positions']
    for pos in positions:
        if float(pos['positionAmt']) != 0:
            data.append(standardize_postion(pos,'binance'))

    data_pd = pd.DataFrame(data)
    print(data_pd)
    st.write(data_pd)
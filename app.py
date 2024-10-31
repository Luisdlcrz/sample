import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go

import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"
import yfinance as yf

import numpy as np

# Specify title and logo for the webpage.
# Set up your web app
st.set_page_config(layout="wide", page_title="WebApp_Demo")

# Sidebar
st.sidebar.title("Input")
symbol = st.sidebar.text_input('Please enter the stock symbol: ', 'NVDA').upper()
# Selection for a specific time frame.
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date',value=datetime.date(2024,1,1))
with col2:
    edate = st.date_input('End Date',value=datetime.date.today())

st.title(f"{symbol}")

stock = yf.Ticker(symbol)
if stock is not None:
  # Display company's basics
  st.write(f"# Sector : {stock.info['sector']}")
  st.write(f"# Company Beta : {stock.info['beta']}")
else:
  st.error("Failed to fetch historical data.")

data = yf.download(symbol,start=sdate,end=edate)
if data is not None:
  st.line_chart(data['Close'],x_label="Date",y_label="Close")
else:
    st.error("Failed to fetch historical data.")

if data.empty:
    st.error("No data found for the specified stock symbol.")
else:
    close_prices = data['Close']
    if not np.issubdtype(close_prices.dtype, np.number):
        st.error("Close price data is not numeric.")
    else:
        if close_prices[0] == 0:
            st.warning("Initial closing price is 0. Using the second value for calculation.")
            growth_rate = (close_prices[-1] - close_prices[1]) / close_prices[1]  
        else:
            growth_rate = (close_prices[-1] - close_prices[0]) / close_prices[0]

        annualized_growth = (1 + growth_rate) ** (365 / len(close_prices)) - 1  

        st.write(f"## Estimated Annualized Growth:")
        st.write(f"{annualized_growth:.2%}") 

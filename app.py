import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import pandas as pd

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

# Display fundamental data
st.write("## Fundamental Data:")

# Create a dictionary of fundamental data to display
fundamentals = {
    "Market Cap": stock.info.get('marketCap', 'N/A'),
    "Trailing P/E": stock.info.get('trailingPE', 'N/A'),
    "Forward P/E": stock.info.get('forwardPE', 'N/A'),
    "Dividend Yield": stock.info.get('dividendYield', 'N/A'),
    "Earnings Growth": stock.info.get('earningsGrowth', 'N/A')
}

for key, value in fundamentals.items():
    st.write(f"{key}: {value}")

# Technical Analysis
st.write("## Technical Analysis:")

data = yf.download(symbol,start=sdate,end=edate)
if data is not None:
  st.write(data.describe())
  st.line_chart(data['Close'],x_label="Date",y_label="Close")
  data = data.reset_index() # Resetting index
  # Calculate Moving Averages
  data['MA20'] = data['Close'].rolling(window=20).mean()  # 20-day MA
  data['MA50'] = data['Close'].rolling(window=50).mean()  # 50-day MA

  # Calculate RSI (Relative Strength Index)
  delta = data['Close'].diff()
  gain = (delta.where(delta > 0, 0)).fillna(0)
  loss = (-delta.where(delta < 0, 0)).fillna(0)
  avg_gain = gain.rolling(window=14).mean()
  avg_loss = loss.rolling(window=14).mean()
  rs = avg_gain / avg_loss
  rsi = 100 - (100 / (1 + rs))
  data['RSI'] = rsi

  st.line_chart(data[['Close', 'MA20', 'MA50']])  # Plot Close, MA20, MA50
  st.line_chart(data['RSI'])  # Plot RSI  
else:
    st.error("Failed to fetch historical data.")

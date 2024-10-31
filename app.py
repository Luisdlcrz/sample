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
    # Add more fundamentals as needed
}


# Technical Analysis
st.write("## Technical Analysis:")

# Handle NaN values (replace with previous valid value)
data['Close'].fillna(method='ffill', inplace=True)

# Calculate Moving Averages
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()


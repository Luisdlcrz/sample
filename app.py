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

st.write("## Company Information:")

# Create a dictionary of company information to display
company_info = {
    "Name": stock.info.get('longName', 'N/A'),
    "Symbol": stock.info.get('symbol', 'N/A'),
    "Website": stock.info.get('website', 'N/A'),
    "Industry": stock.info.get('industry', 'N/A'),
    "Sector": stock.info.get('sector', 'N/A'),
    "Business Summary": stock.info.get('longBusinessSummary', 'N/A')
    # Add more information as needed
}

# Display the company information in a table format
for key, value in company_info.items():
    st.write(f"{key}: {value}")

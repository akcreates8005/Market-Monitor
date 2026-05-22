import streamlit as st
import yfinance as yf # Naya library
from newsapi import NewsApiClient
from textblob import TextBlob

# Page Config
st.set_page_config(page_title="Market Intelligence", layout="wide")

st.title("🚀 MARKET EVOLUTION HUB")

# Stock Search Bar
ticker = st.text_input("🔍 Enter Ticker Symbol (e.g., TSLA, NVDA, AAPL):", "TSLA")

if ticker:
    # 1. Live Stock Data
    stock = yf.Ticker(ticker)
    info = stock.info
    st.subheader(f"📊 Live Data: {ticker}")
    col1, col2 = st.columns(2)
    col1.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
    col2.metric("Market Cap", f"{info.get('marketCap', 0)/1e9:.2f}B")

    # 2. News for that Stock
    st.markdown("---")
    st.subheader(f"🌐 Latest News: {ticker}")
    # (News API ka code waisa hi rahega jaise pehle tha)

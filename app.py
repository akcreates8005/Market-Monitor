import streamlit as st
import pandas as pd
from newsapi import NewsApiClient
from textblob import TextBlob

st.set_page_config(page_title="Market Evolution Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    h2, h3 { color: #00e5ff !important; }
    .stSelectbox > div > div { color: #ffffff !important; background-color: #111111 !important; border: 1px solid #00e5ff !important; }
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #00e5ff !important; }
    div.stMarkdown > div > p { color: #ffffff !important; }
    label, p { color: #ffffff !important; }
    .streamlit-expanderHeader { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

@st.cache_data
def get_market_tickers():
    urls = [
        "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nasdaq/nasdaq_full.csv",
        "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nyse/nyse_full.csv",
        "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/amex/amex_full.csv"
    ]

    stock_list = []

    try:
        for url in urls:
            df = pd.read_csv(url)

            df = df.dropna(subset=["Symbol", "Name"])
            df["Symbol"] = df["Symbol"].astype(str).str.strip()
            df["Name"] = df["Name"].astype(str).str.strip()

            df["Display"] = df["Symbol"] + " - " + df["Name"]
            stock_list.extend(df["Display"].tolist())

        stock_list = sorted(list(set(stock_list)))
        return stock_list

    except Exception as e:
        return [
            "AAPL - Apple Inc.",
            "TSLA - Tesla Inc.",
            "NVDA - NVIDIA Corporation",
            "MSFT - Microsoft Corporation",
            "AMZN - Amazon.com Inc.",
            "AXP - American Express Company",
            "AAL - American Airlines Group Inc."
        ]

all_stocks = get_market_tickers()

selected = st.selectbox(
    "🎯 Search or Select any company:",
    options=[""] + all_stocks,
    index=0
)

if selected:
    ticker = selected.split(" - ")[0]
    company_name = selected.split(" - ", 1)[1]
    search_query = company_name
else:
    ticker = ""
    search_query = ""

if search_query:
    st.subheader(f"🌐 SEARCH RESULTS: {ticker} - {search_query.upper()}")
    query_string = f'"{search_query}" AND (stock OR market OR earnings OR shares)'
else:
    st.subheader("🔥 MARKET PULSE: Top 20 Hyper-News")
    query_string = "(Nvidia OR Tesla OR Apple OR Amazon OR Microsoft) AND (stock OR market OR earnings)"

try:
    articles = newsapi.get_everything(
        q=query_string,
        language="en",
        sort_by="relevancy",
        page_size=45
    )

    if articles and articles.get("articles"):
        for article in articles["articles"]:
            title = article.get("title") or ""
            description = article.get("description") or ""

            analysis = TextBlob(title + " " + description)
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"

            st.markdown(f'<p class="headline">{title}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")

            with st.expander("Click to view details"):
                st.info(description if description else "No summary available.")
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("No major market signals detected.")

except Exception as e:
    st.error("Error fetching news. Please check your API configuration.")

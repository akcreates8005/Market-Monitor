import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

# Page Config
st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Mapping short names to full names for better search results
ticker_mapping = {
    "SLV": "iShares Silver Trust",
    "GLD": "SPDR Gold Shares",
    "SLVP": "iShares MSCI Global Silver Miners",
    "GDX": "VanEck Gold Miners ETF",
    "SIL": "Global X Silver Miners ETF",
    "JEPQ": "JPMorgan Nasdaq Equity Premium Income",
    "QQQI": "Neos Nasdaq 100 High Income",
    "SPYI": "Neos S&P 500 High Income"
}

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    h2, h3 { color: #00ffcc !important; }
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #ffffff !important; }
    div.stMarkdown > div > p { color: #e0e0e0 !important; }
    .streamlit-expanderHeader { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# Combined Dropdown: Sectors + Your specific ticker list
options = ["", "Technology", "Finance", "Healthcare"] + list(ticker_mapping.keys()) + ["NVIDIA", "Tesla", "Apple", "Netflix", "Microsoft", "Amazon"]
selected_item = st.selectbox("🎯 Select or type a Ticker/Sector:", options)

# If selected item is in our mapping, use the full name for the search query
query_term = ticker_mapping.get(selected_item, selected_item)

# Logic
target_list = [query_term] if selected_item else ["Technology", "Finance", "Healthcare"]

for item in target_list:
    st.markdown("---")
    st.subheader(f"🌐 MARKET SIGNALS: {item}")
    
    # NewsAPI Call using the query_term
    articles = newsapi.get_everything(
        q=f"{item} AND (stock OR market OR fund OR ETF)",
        domains='bloomberg.com,reuters.com,cnbc.com,wsj.com',
        language='en',
        sort_by='publishedAt',
        page_size=8
    )
    
    if articles['articles']:
        for article in articles['articles']:
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")
            
            with st.expander("Click to view available details"):
                st.markdown("### Summary")
                st.info(article['description'] if article['description'] else "No detailed summary available.")                
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("No active signals found for this search.")

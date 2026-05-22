import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Enhanced Styling for Professional Look
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #ffffff !important; }
    div.stMarkdown > div > p { color: #e0e0e0 !important; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# User Input for any Ticker or Company Name
search_query = st.text_input("🔍 Enter Ticker (e.g., AAPL) or Company Name:", "").strip()

if search_query:
    st.markdown("---")
    st.subheader(f"🌐 MARKET SIGNALS: {search_query.upper()}")
    
    # Using a broader search query to catch both short tickers and long company names
    # NewsAPI handles "AAPL" or "Apple" effectively when 'stock' is included
    articles = newsapi.get_everything(
        q=f"({search_query}) AND (stock OR merger OR earnings OR dividend)",
        language='en',
        sort_by='publishedAt',
        page_size=10
    )
    
    if articles['articles']:
        for article in articles['articles']:
            # Sentiment Analysis
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")
            
            with st.expander("Click to view details"):
                st.info(article['description'] if article['description'] else "No summary available.")                
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write(f"No major signals for '{search_query}'. Try a broader name or different ticker.")
else:
    st.write("### Please enter a Ticker (e.g., GLD, JEPQ) or Company Name to begin tracking.")

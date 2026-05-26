import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

# Page Config
st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Fixed Styling: Sab kuch wapas Neon/White mein
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    h2, h3 { color: #00e5ff !important; }
    
    /* Search Bar Input Text Color Fix */
    .stTextInput > div > div > input { color: #ffffff !important; background-color: #111111 !important; border: 1px solid #00e5ff !important; }
    
    /* Headlines - Cyan/Aqua Neon */
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #00e5ff !important; }
    
    /* Body text - Bright White */
    div.stMarkdown > div > p { color: #ffffff !important; }
    
    /* Labels (Sentiment etc.) */
    label, p { color: #ffffff !important; }
    
    /* Expander fix */
    .streamlit-expanderHeader { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# Clean Search Bar
search_query = st.text_input("🔍 Search any company or ticker globally (e.g., IBM, American Express, Ford):", "").strip()

# LOGIC
if search_query:
    st.subheader(f"🌐 SEARCH RESULTS: {search_query.upper()}")
    query_string = f"({search_query}) AND (stock OR market OR earnings)"
else:
    st.subheader("🔥 MARKET PULSE: Top 20 Hyper-News")
    query_string = "(Nvidia OR Tesla OR Apple OR SpaceX OR Amazon OR Microsoft OR Google) AND (stock OR market OR earnings)"

# Fetching news
try:
    articles = newsapi.get_everything(
        q=query_string,
        language='en',
        sort_by='relevancy', 
        page_size=30
    )
    
    if articles and articles.get('articles'):
        for article in articles['articles']:
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            # Headline display
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")
            
            with st.expander("Click to view details"):
                st.info(article['description'] or "No summary available.")
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("No results found. Try a different company name.")
except Exception as e:
    st.error("Error fetching news.")

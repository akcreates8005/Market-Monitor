import streamlit as st
from newsapi import NewsApiClient

# Streamlit secrets se API key uthayega
api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("Global Market Intelligence 🌍")

# User se company ka naam mangna
company_input = st.text_input("Konsi company track karni hai? (e.g., NVIDIA, Tesla, Apple):")

# AGAR company name diya hai, toh automatic news dikhaye
if company_input:
    st.subheader(f"Latest News for {company_input}")
    
    # NewsAPI se data fetch karna
    all_articles = newsapi.get_everything(
        q=company_input, 
        language='en', 
        sort_by='publishedAt', 
        page_size=5
    )
    
    if all_articles['totalResults'] > 0:
        for article in all_articles['articles']:
            st.write(f"**{article['title']}**")
            st.write(f"{article['description']}")
            st.write(f"[Read More]({article['url']})")
            st.markdown("---")
    else:
        st.write("Is company ki koi nayi khabar nahi mili.")
else:
    st.write("Upar company ka naam type karo, news apne aap load ho jayegi!")

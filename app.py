!pip install streamlit
import streamlit as st
import pandas as pd
from supabase import create_client, Client

# 🔐 Supabase Connection
url = "https://cakchguemrmvpizmqdka.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNha2NoZ3VlbXJtdnBpem1xZGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ1NDE1NDYsImV4cCI6MjA2MDExNzU0Nn0.aT7Ssu9b--fW39VPhl4fwE2cxSvlw7teZnoFRix4qCE"
supabase: Client = create_client(url, key)

# 📦 Fetch Data
@st.cache_data
def fetch_data():
    response = supabase.table("news_insights").select("*").execute()
    data = response.data
    df = pd.DataFrame(data)
    
    if not df.empty:
        df['published_at'] = pd.to_datetime(df['published_at'])
        df.sort_values(by='published_at', ascending=False, inplace=True)
    return df

df = fetch_data()

# 🧠 Title
st.title("🧠 AI-Driven Competitive Intelligence Tracker")

# 📊 Sidebar Filters
companies = df['Company'].unique().tolist()
selected_companies = st.sidebar.multiselect("Select Companies", companies, default=companies)

# 🔍 Filter Data
filtered_df = df[df["Company"].isin(selected_companies)]

# 📈 Trend Section
st.subheader("📈 Sentiment Trend Over Time (Coming Soon)")

# 📋 News Section
st.subheader("📰 Latest News")

for idx, row in filtered_df.iterrows():
    st.markdown(f"""
    #### {row['title']}
    - 🏢 **Company:** {row['Company']}  
    - 📰 **Source:** {row['source']}  
    - 📅 **Published At:** {row['published_at'].strftime('%Y-%m-%d %H:%M')}  
    - 😊 **Sentiment Score:** `{row['sentiment_score']}`  
    - 🧠 **Top Keywords:** {row['top_keywords']}  
    - 🌐 [Read More]({row['url']})
    ---
    """)
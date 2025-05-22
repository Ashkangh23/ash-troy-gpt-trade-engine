import streamlit as st
import pandas as pd
import datetime
import requests

# --- Load API Key ---
polygon_api_key = st.secrets["polygon"]["api_key"]

# --- Function to Fetch Full Market Snapshot ---
def get_full_market_data():
    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey={polygon_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["tickers"]
        records = []
        for item in data:
            records.append({
                "Ticker": item["ticker"],
                "Last Price": item["lastTrade"].get("p"),
                "Volume": item["day"].get("v"),
                "Change %": item["day"].get("change"),
                "High": item["day"].get("h"),
                "Low": item["day"].get("l"),
                "Open": item["day"].get("o"),
                "Close": item["day"].get("c"),
                "Previous Close": item["prevDay"].get("c"),
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        return pd.DataFrame(records)
    else:
        return pd.DataFrame()

# --- Streamlit UI ---
st.set_page_config(page_title="📊 Full Market Snapshot", layout="wide")
st.title("📊 Real-Time Full U.S. Market Data")
st.caption("Powered by Polygon.io | Download all U.S. stock data in one click")

if st.button("📥 Capture Full Market Snapshot"):
    st.info("Fetching entire U.S. stock market data from Polygon.io...")
    df = get_full_market_data()
    if not df.empty:
        st.success(f"✅ Retrieved {len(df)} tickers with real-time data!")
        st.dataframe(df, use_container_width=True)

        # --- CSV Download ---
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇ Download Full Market CSV",
            data=csv,
            file_name="full_market_snapshot.csv",
            mime="text/csv"
        )
    else:
        st.error("❌ Failed to retrieve market data. Please check your API key or try again later.")

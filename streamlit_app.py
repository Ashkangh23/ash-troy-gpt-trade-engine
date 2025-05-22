import streamlit as st
import pandas as pd
import datetime
import requests

# --- Load API Key ---
polygon_api_key = st.secrets["polygon"]["api_key"]

# --- Function to Fetch Real-Time Data ---
def get_realtime_data(tickers):
    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?tickers={','.join(tickers)}&apiKey={polygon_api_key}"
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
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        return pd.DataFrame(records)
    else:
        return pd.DataFrame()

# --- Streamlit UI ---
st.set_page_config(page_title="Real-Time Market Data App", layout="wide")
st.title("📈 Real-Time Stock Market Data Downloader")
st.caption("Capture and download market data from Polygon.io with updates as close as 5 seconds")

# --- Ticker Input ---
st.markdown("### 🔍 Enter stock ticker symbols (comma-separated)")
ticker_input = st.text_area("Tickers", "AAPL,MSFT,NVDA")

if st.button("🔄 Fetch Real-Time Data"):
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    if tickers:
        st.info("Fetching data from Polygon.io...")
        df = get_realtime_data(tickers)
        if not df.empty:
            st.success("✅ Real-time data retrieved!")
            st.dataframe(df, use_container_width=True)

            # --- CSV Download ---
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="realtime_market_data.csv",
                mime="text/csv"
            )
        else:
            st.error("❌ Failed to retrieve data. Check your API key or ticker symbols.")


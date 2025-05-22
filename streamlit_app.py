import streamlit as st
import openai
import pandas as pd
import datetime
import requests

# --- Load API Keys ---
polygon_api_key = st.secrets["polygon"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]
openai.api_key = openai_api_key

# --- GPT System Prompt ---
SYSTEM_PROMPT = """
Ash’s TGN Trade Engine GPT acts strictly as a real-time institutional-grade market research assistant. It monitors all media channels and live data feeds, focusing on S&P 500, NASDAQ, Dow, Russell, and Magnificent 7. It scans both large- and small-cap stocks and shadows institutional and mid-tier firms.

It follows these trading principles:
- Only trades long positions
- Avoids buying on up days and selling on down days
- Buys on double bottom signals, avoids double tops
- Filters trades using: Volume Surge ≥1.5× 20-day avg, MACD bullish crossover, RSI 30–60, Buy Zone alignment, Volume ≥500K
- Applies Signal Score and outputs only institutional-quality trade sheets
- Never includes commentary — only formatted output
"""

# --- Streamlit UI ---
st.set_page_config(page_title="Ash&Troy GPT Trade Engine", layout="wide")
st.title("🚀 Ash&Troy GPT Trade Engine")
st.caption("Live GPT-driven market scanner using real-time Polygon.io data")

st.markdown("### 💬 Enter a trading prompt to apply your Custom GPT's strategy...")
st.info("Examples: 'Find energy stocks with RSI < 50 and MACD bullish crossover', 'Show long trade setups with volume surge'")

# --- Chat Prompt ---
user_prompt = st.chat_input("Enter your trade query here...")

if user_prompt:
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.spinner("Using Custom GPT logic to interpret your strategy..."):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        gpt_response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.4
        )
        parsed_query = gpt_response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(parsed_query)

    with st.spinner("Fetching filtered trades using Custom GPT logic..."):
        # Placeholder: Replace this with real-time filtering logic
        data = {
            "Ticker": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"],
            "Signal Score": [95, 92, 90, 88, 85],
            "Buy/Sell Day": ["Buy"] * 5,
            "Execution Readiness": ["High"] * 5,
            "Entry Range": ["$170-172", "$310-312", "$900-910", "$140-145", "$120-123"],
            "Risk/Reward Ratio": [2.8, 2.5, 3.0, 2.0, 2.2],
            "Volume Class": ["High"] * 5,
            "RSI": [44, 47, 39, 42, 45],
            "MACD": ["Bullish"] * 5,
            "Price": ["$171", "$311", "$905", "$142", "$121"],
            "Timestamp": [datetime.datetime.now().isoformat()] * 5
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

    with st.expander("📊 Refine further using GPT intelligence"):
        followup = st.text_area("Ask GPT to re-analyze or break down this data:")
        if followup:
            refined = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": parsed_query},
                    {"role": "user", "content": followup}
                ],
                temperature=0.5
            )
            st.markdown(refined.choices[0].message.content)


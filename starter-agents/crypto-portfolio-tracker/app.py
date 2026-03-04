import streamlit as st
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(
    page_title="Crypto Portfolio Tracker",
    page_icon="📊",
    layout="wide"
)

CRYPTO_API = "https://agent-gateway-kappa.vercel.app/v1/crypto-feeds/api/prices"


def get_crypto_prices():
    """Fetch real-time crypto prices from free API (no auth required)."""
    try:
        resp = requests.get(CRYPTO_API, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("prices", {})
    except Exception as e:
        st.error(f"Error fetching prices: {e}")
        return {}


def calculate_portfolio(holdings, prices):
    """Calculate portfolio value from holdings and current prices."""
    results = []
    total = 0.0
    for symbol, amount in holdings.items():
        symbol_upper = symbol.upper()
        price_info = prices.get(symbol_upper)
        if price_info:
            price = float(price_info.get("price", 0))
            value = price * amount
            total += value
            results.append({
                "symbol": symbol_upper,
                "amount": amount,
                "price": price,
                "value": value,
            })
    return results, total


def get_ai_analysis(portfolio_data, total_value, api_key, model):
    """Get AI-powered portfolio analysis."""
    client = OpenAI(api_key=api_key)

    portfolio_text = "\n".join(
        f"- {p['symbol']}: {p['amount']} units @ ${p['price']:.2f} = ${p['value']:.2f} "
        f"({p['value']/total_value*100:.1f}%)"
        for p in portfolio_data
    )

    prompt = f"""Analyze this crypto portfolio (total value: ${total_value:,.2f}):

{portfolio_text}

Provide a brief analysis covering:
1. Portfolio concentration risk
2. Asset allocation observations
3. One actionable suggestion"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a crypto portfolio analyst. Be concise and practical."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content


def main():
    st.title("📊 Crypto Portfolio Tracker")
    st.caption("Track your crypto portfolio with real-time prices and AI analysis")

    if "holdings" not in st.session_state:
        st.session_state.holdings = {"BTC": 0.5, "ETH": 5.0, "SOL": 100.0}

    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input(
            "OpenAI API Key (optional, for AI analysis)",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
        )
        model = st.selectbox("Model", ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"])

        st.divider()
        st.header("💰 Edit Holdings")

        new_symbol = st.text_input("Token symbol", placeholder="e.g. BTC").upper()
        new_amount = st.number_input("Amount", min_value=0.0, step=0.01)
        if st.button("Add / Update") and new_symbol:
            st.session_state.holdings[new_symbol] = new_amount
            st.rerun()

        if st.session_state.holdings:
            to_remove = st.selectbox(
                "Remove token",
                [""] + list(st.session_state.holdings.keys()),
            )
            if st.button("Remove") and to_remove:
                del st.session_state.holdings[to_remove]
                st.rerun()

    prices = get_crypto_prices()
    if not prices:
        st.warning("Could not fetch prices. Please try again.")
        return

    portfolio_data, total_value = calculate_portfolio(st.session_state.holdings, prices)

    col1, col2, col3 = st.columns(3)
    col1.metric("Portfolio Value", f"${total_value:,.2f}")
    col2.metric("Assets Tracked", len(portfolio_data))
    col3.metric("Prices Available", len(prices))

    st.subheader("Your Portfolio")
    if portfolio_data:
        for item in sorted(portfolio_data, key=lambda x: x["value"], reverse=True):
            pct = item["value"] / total_value * 100 if total_value > 0 else 0
            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 1])
            col_a.write(f"**{item['symbol']}**")
            col_b.write(f"{item['amount']} units")
            col_c.write(f"${item['value']:,.2f}")
            col_d.write(f"{pct:.1f}%")
    else:
        st.info("Add tokens in the sidebar to track your portfolio.")

    if api_key and portfolio_data:
        st.divider()
        if st.button("🤖 Get AI Analysis"):
            with st.spinner("Analyzing portfolio..."):
                try:
                    analysis = get_ai_analysis(portfolio_data, total_value, api_key, model)
                    st.markdown("### AI Analysis")
                    st.markdown(analysis)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

    st.divider()
    st.subheader("Live Market Prices")
    top_tokens = ["BTC", "ETH", "SOL", "DOGE", "XRP", "ADA", "AVAX", "DOT", "MATIC", "LINK"]
    cols = st.columns(5)
    for i, symbol in enumerate(top_tokens):
        info = prices.get(symbol, {})
        price = float(info.get("price", 0))
        if price > 0:
            cols[i % 5].metric(symbol, f"${price:,.2f}")


if __name__ == "__main__":
    main()

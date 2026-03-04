# Crypto Portfolio Tracker

A real-time crypto portfolio tracker with AI-powered analysis, built with Streamlit and OpenAI GPT-4. Uses a free crypto price API with 275+ tokens — no API key required for price data.

## Features

- Real-time prices for 275+ crypto assets (BTC, ETH, SOL, and more)
- Portfolio tracking with value calculation and allocation percentages
- AI-powered portfolio analysis (concentration risk, allocation, suggestions)
- Live market dashboard for top tokens
- Add/remove tokens and adjust holdings

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4 (optional, for AI analysis)
- **Price Data**: [Free Crypto Price API](https://agent-gateway-kappa.vercel.app/v1/crypto-feeds/api/prices) (no auth required)
- **Language**: Python 3.8+

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables** (optional, for AI analysis):
   ```bash
   echo "OPENAI_API_KEY=your-key-here" > .env
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** at `http://localhost:8501`

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI analysis | No |

The crypto price data is free and requires no API key. AI analysis is optional.

## How It Works

1. Fetches real-time prices from a free REST API (275+ tokens via Hyperliquid)
2. Calculates portfolio value based on your holdings
3. Optionally sends portfolio data to GPT-4 for concentration and risk analysis
4. Displays a live market dashboard with top token prices

## License

MIT License

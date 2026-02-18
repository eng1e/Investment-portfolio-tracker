import streamlit as st
import yfinance as yf
import pandas as pd
st.title("Investment Portfolio Risk Dashboard")
assets = ["AAPL", "MSFT", "TSLA", "NVDA", "SPY", "GLD", "BTC-USD"]

data = yf.download(assets, start="2023-01-01")["Close"]
st.subheader("Assets Prices")
st.line_chart(data)

#حساب النسبة المئوية لتغير السعر يوميا
returns = data.pct_change()
st.subheader("Daily Returns")
st.line_chart(returns)

cumulative = (1 + returns).cumprod()
st.subheader("Cumulative Returns")
st.line_chart(cumulative)

import numpy as np
volatility = returns.std() * np.sqrt(252)
st.subheader("Volatility (Risk)")
st.bar_chart(volatility)

sharpe = returns.mean() / returns.std() * np.sqrt(252)
st.subheader("Sharpe Ratio")
st.bar_chart(sharpe)

st.subheader("Key Insights")
st.write("""
         -Tesla (TSLA)
         -Gold (GLD)
         -Diversified portfolio
         """)

selected_assets = st.multiselect(
    "Select Assets to Display",
    options=assets,
    default=assets
)
data_selected = data[selected_assets]
returns_selected = returns[selected_assets]
cumulative_selected = cumulative[selected_assets]
volatility_selected = volatility[selected_assets]
sharpe_selected = sharpe[selected_assets]

st.subheader("Selected Assets Prices")
st.line_chart(data_selected)

st.subheader("Selected Daily Returns")
st.line_chart(returns_selected)

st.subheader("Portofolio Weights")
weights = []
for asset in selected_assets:
    w = st.slider(f"Weight for {asset}(%)", 0, 100, 100//len(selected_assets))
    weights.append(w/100)

weights = [w/sum(weights) for w in weights]

portfolio_returns = (returns_selected * weights).sum(axis=1)
portfolio_cumulative = (1 + portfolio_returns).cumprod()
portfolio_volatility = portfolio_returns.std() * np.sqrt(252)
portfolio_sharpe = (portfolio_returns.mean() / portfolio_returns.std()) * np.sqrt(252)

st.subheader("Portfolio Cumulative Returns")
st.line_chart(portfolio_cumulative)

st.write(f"Portfolio Volatility (Risk): {portfolio_volatility:.2%}")
st.write(f"portfolio Sharpe Ratio: {portfolio_sharpe:.2f}")


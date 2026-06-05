import streamlit as st
import yfinance as yf

# 1. Page Configuration
st.set_page_config(page_title="SET50", page_icon="📈", layout="centered")
st.title("📈 SET50 Stock Monitor")

# List of SET50 Stocks (Alphabetical Order)
set50_stocks = sorted([
    'ADVANC', 'AOT', 'AWC', 'BBL', 'BDMS', 'BEM', 'BGRIM', 'BH', 'BJC', 'BTS', 
    'CBG', 'CENTEL', 'CPALL', 'CPF', 'CPN', 'CRC', 'DELTA', 'EA', 'EGCO', 'GLOBAL', 
    'GPSC', 'GULF', 'HMPRO', 'INTUCH', 'IRPC', 'IVL', 'KBANK', 'KCE', 'KTB', 'KTC', 
    'LH', 'MINT', 'OR', 'OSP', 'PTT', 'PTTEP', 'PTTGC', 'RATCH', 'SAWAD', 'SCB', 
    'SCC', 'SCGP', 'TISCO', 'TKN', 'TOP', 'TRUE', 'TTB', 'TU', 'WHA', 'WHAUP'
])
timeframes = {'1M': '1mo', '3M': '3mo', '6M': '6mo', '1Y': '1y', '3Y': '3y'}

# 2. Initialize Memory (Session State for Buttons)
if 'active_stock' not in st.session_state:
    st.session_state.active_stock = 'PTT'
if 'active_tf' not in st.session_state:
    st.session_state.active_tf = '1M'

# 3. UI: Timeframe Buttons
st.subheader("Select Timeframe")
tf_cols = st.columns(len(timeframes))
for i, tf in enumerate(timeframes.keys()):
    if tf_cols[i].button(tf, use_container_width=True):
        st.session_state.active_tf = tf

st.markdown("---")

# 4. UI: SET50 Stock Buttons
st.subheader("Select SET50 Stock")
st.write(f"**Currently Selected:** {st.session_state.active_stock} | **Timeframe:** {st.session_state.active_tf}")

# Use expander to prevent the screen from being too long on mobile
with st.expander("Click to expand/collapse SET50 buttons", expanded=False):
    cols = st.columns(5) # 5 columns grid
    for i, stock in enumerate(set50_stocks):
        if cols[i % 5].button(stock, use_container_width=True):
            st.session_state.active_stock = stock

st.markdown("---")

# 5. Fetch Data from Yahoo Finance
ticker_symbol = f"{st.session_state.active_stock}.BK"
period_val = timeframes[st.session_state.active_tf]

with st.spinner(f'Fetching data for {st.session_state.active_stock}...'):
    stock_data = yf.Ticker(ticker_symbol)
    hist = stock_data.history(period=period_val)

# 6. Calculate and Display Results
if not hist.empty:
    current_price = hist['Close'].iloc[-1]
    past_price = hist['Close'].iloc[0]
    change = current_price - past_price
    pct_change = (change / past_price) * 100

    st.metric(
        label=f"{st.session_state.active_stock} - Current Price", 
        value=f"THB {current_price:.2f}", 
        delta=f"{change:.2f} ({pct_change:.2f}%)"
    )

    st.line_chart(hist['Close'])
else:
    st.error("Unable to fetch data at this time. The market might be updating or the symbol has no data.")

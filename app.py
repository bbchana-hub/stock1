import streamlit as st
import yfinance as yf

# 1. Page Configuration
st.set_page_config(page_title="SET50 Stock Monitor", page_icon="📈", layout="centered")
st.title("📈 SET50 Stock Monitor")

# List of SET50 Stocks
set50_stocks = sorted([
    'ADVANC', 'AOT', 'AWC', 'BBL', 'BDMS', 'BEM', 'BGRIM', 'BH', 'BJC', 'BTS', 
    'CBG', 'CENTEL', 'CPALL', 'CPF', 'CPN', 'CRC', 'DELTA', 'EA', 'EGCO', 'GLOBAL', 
    'GPSC', 'GULF', 'HMPRO', 'INTUCH', 'IRPC', 'IVL', 'KBANK', 'KCE', 'KTB', 'KTC', 
    'LH', 'MINT', 'OR', 'OSP', 'PTT', 'PTTEP', 'PTTGC', 'RATCH', 'SAWAD', 'SCB', 
    'SCC', 'SCGP', 'TISCO', 'TKN', 'TOP', 'TRUE', 'TTB', 'TU', 'WHA', 'WHAUP'
])

# Timeframe mapping for Slider
timeframes = ['1M', '3M', '6M', '1Y', '3Y']
tf_mapping = {'1M': '1mo', '3M': '3mo', '6M': '6mo', '1Y': '1y', '3Y': '3y'}

# 2. Initialize Memory for Stock Selection
if 'active_stock' not in st.session_state:
    st.session_state.active_stock = 'PTT'

# ==========================================
# ROW 1: Stock Buttons
# ==========================================
st.subheader("1. Select SET50 Stock")
with st.expander("Click to view all SET50 stocks", expanded=False):
    cols = st.columns(5)
    for i, stock in enumerate(set50_stocks):
        if cols[i % 5].button(stock, use_container_width=True):
            st.session_state.active_stock = stock

st.markdown("<br>", unsafe_allow_html=True) # Add some spacing

# ==========================================
# ROW 2: Timeframe Slider
# ==========================================
st.subheader("2. Select Timeframe")
selected_tf = st.select_slider(
    "Slide to change period:",
    options=timeframes,
    value='1M',
    label_visibility="collapsed" # Hide the default label for a cleaner UI
)

st.markdown("---")

# 3. Display Current Selection
st.write(f"**Monitoring:** {st.session_state.active_stock} | **Period:** {selected_tf}")

# 4. Fetch Data from Yahoo Finance
ticker_symbol = f"{st.session_state.active_stock}.BK"
period_val = tf_mapping[selected_tf]

with st.spinner(f'Fetching data for {st.session_state.active_stock}...'):
    stock_data = yf.Ticker(ticker_symbol)
    hist = stock_data.history(period=period_val)

# 5. Calculate and Display Results
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

import streamlit as st
import yfinance as yf

# 1. Page Configuration
st.set_page_config(page_title="Thai Stock Monitor", page_icon="📈")
st.title("📈 Thai Stock Monitor")

# 2. User Selections
stocks = {'PTT': 'PTT.BK', 'SCB': 'SCB.BK', 'TISCO': 'TISCO.BK'}
timeframes = {'1 Month': '1mo', '3 Months': '3mo', '6 Months': '6mo', '1 Year': '1y', '3 Years': '3y'}

col1, col2 = st.columns(2)
with col1:
    selected_name = st.selectbox("Select Stock", list(stocks.keys()))
with col2:
    selected_tf_name = st.selectbox("Select Timeframe", list(timeframes.keys()))

# 3. Fetch Data from Yahoo Finance
ticker = stocks[selected_name]
period = timeframes[selected_tf_name]

# Add loading spinner
with st.spinner('Fetching data...'):
    stock_data = yf.Ticker(ticker)
    hist = stock_data.history(period=period)

# 4. Calculate and Display Results
if not hist.empty:
    current_price = hist['Close'].iloc[-1]
    past_price = hist['Close'].iloc[0]
    change = current_price - past_price
    pct_change = (change / past_price) * 100

    # Display price and profit/loss metrics
    st.metric(
        label=f"Current Price: {selected_name}", 
        value=f"฿{current_price:.2f}", 
        delta=f"{change:.2f} ({pct_change:.2f}%)"
    )

    # Draw line chart
    st.line_chart(hist['Close'])
else:
    st.error("Unable to fetch data at this time.")

import streamlit as st
import yfinance as yf

# 1. à¸•à¸±à¹‰à¸‡à¸„à¹ˆà¸²à¸«à¸™à¹‰à¸²à¹€à¸§à¹‡à¸š
st.set_page_config(page_title="Thai Stock Monitor", page_icon="ðŸ“ˆ")
st.title("ðŸ“ˆ Thai Stock Monitor")

# 2. à¸ªà¸£à¹‰à¸²à¸‡à¸•à¸±à¸§à¹€à¸¥à¸·à¸­à¸à¹ƒà¸«à¹‰à¸œà¸¹à¹‰à¹ƒà¸Šà¹‰à¸‡à¸²à¸™
stocks = {'à¸›à¸•à¸—. (PTT)': 'PTT.BK', 'à¹€à¸­à¸ªà¸‹à¸µà¸šà¸µ à¹€à¸­à¸à¸‹à¹Œ (SCB)': 'SCB.BK', 'à¸—à¸´à¸ªà¹‚à¸à¹‰ (TISCO)': 'TISCO.BK'}
timeframes = {'1 à¹€à¸”à¸·à¸­à¸™': '1mo', '3 à¹€à¸”à¸·à¸­à¸™': '3mo', '6 à¹€à¸”à¸·à¸­à¸™': '6mo', '1 à¸›à¸µ': '1y', '3 à¸›à¸µ': '3y'}

col1, col2 = st.columns(2)
with col1:
    selected_name = st.selectbox("à¹€à¸¥à¸·à¸­à¸à¸«à¸¸à¹‰à¸™", list(stocks.keys()))
with col2:
    selected_tf_name = st.selectbox("à¹€à¸¥à¸·à¸­à¸à¸Šà¹ˆà¸§à¸‡à¹€à¸§à¸¥à¸²", list(timeframes.keys()))

# 3. à¸”à¸¶à¸‡à¸‚à¹‰à¸­à¸¡à¸¹à¸¥à¸ˆà¸²à¸ Yahoo Finance
ticker = stocks[selected_name]
period = timeframes[selected_tf_name]

# à¹ƒà¸ªà¹ˆ Spinner à¸«à¸¡à¸¸à¸™à¹† à¸•à¸­à¸™à¸à¸³à¸¥à¸±à¸‡à¹‚à¸«à¸¥à¸”
with st.spinner('à¸à¸³à¸¥à¸±à¸‡à¸”à¸¶à¸‡à¸‚à¹‰à¸­à¸¡à¸¹à¸¥...'):
    stock_data = yf.Ticker(ticker)
    hist = stock_data.history(period=period)

# 4. à¸„à¸³à¸™à¸§à¸“à¹à¸¥à¸°à¹à¸ªà¸”à¸‡à¸œà¸¥
if not hist.empty:
    current_price = hist['Close'].iloc[-1]
    past_price = hist['Close'].iloc[0]
    change = current_price - past_price
    pct_change = (change / past_price) * 100

    # à¹à¸ªà¸”à¸‡à¸•à¸±à¸§à¹€à¸¥à¸‚à¸£à¸²à¸„à¸²à¹à¸¥à¸°à¸à¸³à¹„à¸£/à¸‚à¸²à¸”à¸—à¸¸à¸™
    st.metric(
        label=f"à¸£à¸²à¸„à¸²à¸›à¸±à¸ˆà¸ˆà¸¸à¸šà¸±à¸™ {selected_name}", 
        value=f"à¸¿{current_price:.2f}", 
        delta=f"{change:.2f} ({pct_change:.2f}%)"
    )

    # à¸§à¸²à¸”à¸à¸£à¸²à¸Ÿà¹€à¸ªà¹‰à¸™à¸ªà¸§à¸¢à¹†
    st.line_chart(hist['Close'])
else:
    st.error("à¹„à¸¡à¹ˆà¸ªà¸²à¸¡à¸²à¸£à¸–à¸”à¸¶à¸‡à¸‚à¹‰à¸­à¸¡à¸¹à¸¥à¹„à¸”à¹‰à¹ƒà¸™à¸‚à¸“à¸°à¸™à¸µà¹‰")

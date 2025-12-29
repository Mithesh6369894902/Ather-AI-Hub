import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from datetime import datetime

def safe_float(x):
    try:
        return float(x)
    except Exception:
        return 0.0


# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AlphaFlux",
    page_icon="🧠📈",
    layout="wide"
)

st.title("🧠📈 AlphaFlux")
st.caption("Risk-Aware Stock Trend Forecasting & Decision Intelligence")

# ---------------- UTILITIES ----------------
@st.cache_data
def load_stock(symbol, start, end):
    return yf.download(symbol, start=start, end=end)

def prepare_features(df):
    df = df.copy()
    df["TimeIndex"] = np.arange(len(df))
    return df

def linear_trend_model(df):
    X = df[["TimeIndex"]]
    y = df["Close"]
    model = LinearRegression()
    model.fit(X, y)
    return model

def rolling_trend(df, window=20):
    return df["Close"].rolling(window).mean()

def forecast(model, start_idx, horizon):
    future_idx = np.arange(start_idx, start_idx + horizon).reshape(-1, 1)
    return model.predict(future_idx)

def cross_validated_error(df):
    tscv = TimeSeriesSplit(n_splits=5)
    errors = []

    for train, test in tscv.split(df):
        model = LinearRegression()
        X_train = df.iloc[train][["TimeIndex"]]
        y_train = df.iloc[train]["Close"]
        X_test = df.iloc[test][["TimeIndex"]]
        y_test = df.iloc[test]["Close"]

        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        errors.append(np.mean(np.abs(pred - y_test)))

    return np.mean(errors)

def safe_float(x):
    try:
        return float(x)
    except Exception:
        return 0.0

def generate_signal(recent_price, predicted_price, uncertainty):
    r = safe_float(recent_price)
    p = safe_float(predicted_price)
    u = safe_float(uncertainty)

    delta = p - r
    risk_score = delta / (u + 1e-6)

    if risk_score > 0.5:
        return "📈 BUY", risk_score
    elif risk_score < -0.5:
        return "📉 SELL", risk_score
    else:
        return "⏸ HOLD", risk_score




# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

symbol = st.sidebar.text_input("Stock Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.today())
forecast_horizon = st.sidebar.slider("Forecast Days", 5, 60, 20)

# ---------------- DATA ----------------
data = load_stock(symbol, start_date, end_date)

if data.empty:
    st.error("No data available.")
    st.stop()

data = prepare_features(data)

# ---------------- MODELING ----------------
model = linear_trend_model(data)
future_prices = forecast(model, data["TimeIndex"].iloc[-1] + 1, forecast_horizon)

cv_error = cross_validated_error(data)

recent_avg = data["Close"].tail(10).mean()
future_avg = np.mean(future_prices)

signal, confidence = generate_signal(recent_avg, future_avg, cv_error)

# ---------------- VISUALIZATION ----------------
st.subheader("📊 Price Trend Analysis")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(data.index, data["Close"], label="Historical Close", color="blue")

future_dates = pd.date_range(
    start=data.index[-1],
    periods=forecast_horizon + 1,
    freq="B"
)[1:]

ax.plot(future_dates, future_prices, "--", label="Forecast", color="orange")
ax.set_title(f"{symbol} Price Trend")
ax.legend()
st.pyplot(fig)

# ---------------- RESULTS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Recent Avg Price", f"${recent_avg_f:.2f}")
col2.metric("Predicted Avg Price", f"${future_avg_f:.2f}")
col3.metric("Model Uncertainty (MAE)", f"${cv_error_f:.2f}")


st.subheader("🧠 Decision Intelligence")

st.markdown(f"""
### **Trading Signal:** {signal}

- **Risk-adjusted confidence score:** `{confidence:.2f}`
- **Interpretation:**  
  This recommendation considers **trend strength relative to historical prediction error**.
""")

# ---------------- TABLE ----------------
st.subheader("🔮 Forecast Table")

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted Price": future_prices
})

st.dataframe(forecast_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚠️ Educational use only. Not financial advice.")

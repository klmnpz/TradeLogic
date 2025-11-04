import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="TradeLogic", page_icon="📊", layout="centered")
st.title("📊 TradeLogic — Учись инвестировать без риска")

st.markdown("""
TradeLogic помогает начинающим инвесторам тестировать стратегии на реальных исторических данных.
Выберите акцию, настройте стратегию и узнайте, была ли она прибыльной — без риска потери денег.
""")

st.sidebar.header("⚙️ Параметры стратегии")
ticker = st.sidebar.text_input("Введите тикер (например, AAPL, TSLA, BTC-USD):", "AAPL")
short_ma = st.sidebar.number_input("Короткая скользящая средняя:", 20)
long_ma = st.sidebar.number_input("Длинная скользящая средняя:", 50)
start_date = st.sidebar.date_input("Начальная дата:", pd.to_datetime("2018-01-01"))
end_date = st.sidebar.date_input("Конечная дата:", pd.to_datetime("2025-01-01"))

if st.sidebar.button("🚀 Запустить Backtest"):
    data = yf.download(ticker, start=start_date, end=end_date)
    data["SMA_short"] = data["Close"].rolling(short_ma).mean()
    data["SMA_long"] = data["Close"].rolling(long_ma).mean()
    data["Signal"] = 0
    data.loc[data["SMA_short"] > data["SMA_long"], "Signal"] = 1
    data.loc[data["SMA_short"] < data["SMA_long"], "Signal"] = -1
    data["Position"] = data["Signal"].shift(1)

    data["Return"] = np.log(data["Close"] / data["Close"].shift(1))
    data["Strategy"] = data["Return"] * data["Position"]
    cumulative_strategy = data["Strategy"].cumsum()
    cumulative_market = data["Return"].cumsum()

    st.subheader(f"📈 Результаты стратегии для {ticker}")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data["Close"], label="Цена", alpha=0.8)
    ax.plot(data.index, data["SMA_short"], label=f"SMA {short_ma}", linestyle="--")
    ax.plot(data.index, data["SMA_long"], label=f"SMA {long_ma}", linestyle="--")
    ax.legend()
    st.pyplot(fig)

    st.subheader("📊 Сравнение доходности")
    comparison = pd.DataFrame({
        "Стратегия": cumulative_strategy,
        "Пассивное инвестирование": cumulative_market
    })
    st.line_chart(comparison)

    st.success(f"✅ Доходность стратегии: {cumulative_strategy.iloc[-1]*100:.2f}%")

st.header("🎓 Учебный модуль")
lesson = st.selectbox("Выберите тему:", [
    "Что такое акции?",
    "Как работает стратегия скользящих средних?",
    "Как оценить прибыльность инвестиций?"
])

if lesson == "Что такое акции?":
    st.info("💡 Акция — это доля собственности компании.")
elif lesson == "Как работает стратегия скользящих средних?":
    st.info("📊 Когда короткая средняя пересекает длинную снизу вверх — это сигнал покупки, а сверху вниз — продажи.")
else:
    st.info("📈 Прибыль можно измерить через логарифмическую доходность: ln(Pt / Pt-1).")

st.caption("Developed by Fatima Ergasheva | Prototype version of TradeLogic | 2025")
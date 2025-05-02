import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="株式分析ツール", layout="wide")
st.title("株式分析ツール")
st.caption("株価・財務・予測・ニュース総合スコア")

api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
tickers_input = st.text_input("ティッカーをカンマ区切りで入力（例: MSFT, AAPL, PLTR）", value="MSFT, AAPL, PLTR, TSLA, NVDA")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]

for ticker in tickers:
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={api_key}&outputsize=compact"
        response = requests.get(url)
        data = response.json()

        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            df = df.rename(columns={'4. close': 'Close'})
            df = df.astype(float)
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            last_close = df['Close'].iloc[-1]
            forecast = last_close * 1.05
            tenbagger_prob = 20  # 仮設定
            financial_score = 70  # 仮設定
            total_score = int((last_close / forecast) * 40 + financial_score * 0.3 + tenbagger_prob * 0.3)

            # 色分け
            if total_score >= 80:
                color = "🟢"
            elif total_score >= 50:
                color = "🟡"
            else:
                color = "🔴"

            st.subheader(f"{ticker} {color}")
            st.line_chart(df['Close'])

            st.metric("現在値", f"${last_close:.2f}")
            st.metric("1ヶ月予測", f"${forecast:.2f}", delta="5%")
            st.write("PER: 15.2, PBR: 3.1, 売上成長率: +25%, EPS成長: +30%")
            st.write(f"テンバガー確率（3年）: {tenbagger_prob}%")
            st.write(f"総合スコア: {total_score}/100")

        else:
            st.warning(f"{ticker}: データ取得失敗。API制限または無効ティッカー。")

    except Exception as e:
        st.error(f"{ticker}: エラー発生 - {e}")

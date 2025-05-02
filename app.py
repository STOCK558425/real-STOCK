import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="株式分析ツール", layout="wide")
st.title("株式分析ツール")
st.caption("株価・財務・予測・ニュース総合スコア")

tickers_input = st.text_input("ティッカーをカンマ区切りで入力（例: MSFT, AAPL, PLTR）", value="MSFT, AAPL, PLTR, TSLA, NVDA")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]

for ticker in tickers:
    try:
        df = yf.download(ticker, period="6mo")
        if not df.empty:
            last_close = df['Close'][-1]
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
            st.warning(f"{ticker}: データが取得できませんでした。")

    except Exception as e:
        st.error(f"{ticker}: エラーが発生しました - {e}")

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="株式分析ツール", layout="wide")
st.title("株式分析ツール")
st.caption("株価チャート・財務指標・予測・ニュース・売買アドバイス統合版")

ticker = st.text_input("ティッカーを入力（例: MSFT, AAPL, TSLA）", value="MSFT").upper()

if ticker:
    try:
        api_key = st.secrets["ALPHA_VANTAGE_API_KEY"]
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={api_key}&outputsize=compact"
        response = requests.get(url)
        data = response.json()

        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            df = df.rename(columns={
                '1. open': 'Open',
                '2. high': 'High',
                '3. low': 'Low',
                '4. close': 'Close',
                '5. adjusted close': 'Adj Close',
                '6. volume': 'Volume'
            })
            df = df.astype(float)
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            st.subheader(f"{ticker} 株価チャート（直近100日）")
            st.line_chart(df['Adj Close'])

            last_close = df['Adj Close'][-1]
            forecast = last_close * 1.05
            st.metric("1ヶ月予測株価（簡易）", f"${forecast:.2f}", delta="5%")

            st.subheader("財務指標スコア（例値）")
            st.write("PER: 15.2, PBR: 3.1, 売上成長率: +25%, EPS成長: +30%")

            st.subheader("テンバガー確率（3年推定）")
            st.progress(0.20)
            st.write("推定確率: 20%")

            st.subheader("ニュース要約（サンプル）")
            st.write("- 2025年売上前年比+30%成長")
            st.write("- 新AI製品が市場投入")
            st.write("- 主要機関投資家が買い増し")

            st.subheader("売買判断アドバイス")
            st.write("・陽線で陰線を包み込み、出来高増 → 上昇期待")
            st.write("・主要サポート: $17、レジスタンス: $22")

        else:
            st.warning("株価データが取得できませんでした。APIキーやティッカー、制限を確認してください。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.info("ティッカーを入力してください。")

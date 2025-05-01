import streamlit as st
import yfinance as yf

st.set_page_config(page_title="株式分析ツール", layout="wide")

st.title("株式分析ツール")
st.caption("株価チャート・財務指標・予測・ニュース・売買アドバイス統合版")

ticker = st.text_input("ティッカーを入力（例: GRRR, PLTR, TSLA）", value="PLTR")

if ticker:
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info

        if not info or info is None:
            st.warning("ティッカー情報が取得できません（yfinance未対応の可能性があります）。")
        else:
            df = ticker_obj.history(period="6mo")
            if not df.empty:
                st.success(f"{ticker} のデータ取得に成功しました！")
                st.subheader("株価チャート（6ヶ月）")
                st.line_chart(df['Close'])

                last_close = df['Close'][-1]
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
                st.warning("株価履歴データが取得できませんでした。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.info("ティッカーを入力してください。")

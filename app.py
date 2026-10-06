import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="AI Trader",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI TRADER")
st.caption("Analisador de ações — modo simulação")

acoes = {
    "PETR4": "PETR4.SA",
    "VALE3": "VALE3.SA",
    "ITUB4": "ITUB4.SA",
    "BBAS3": "BBAS3.SA"
}

acao = st.selectbox("Escolha uma ação:", list(acoes.keys()))

if st.button("🔍 ANALISAR"):

    dados = yf.download(
        acoes[acao],
        period="1y",
        auto_adjust=False,
        progress=False
    )

    fechamento = dados["Close"]

    if isinstance(fechamento, pd.DataFrame):
        fechamento = fechamento.iloc[:, 0]

    m20 = fechamento.rolling(20).mean()
    m50 = fechamento.rolling(50).mean()

    delta = fechamento.diff()
    ganhos = delta.clip(lower=0)
    perdas = -delta.clip(upper=0)

    media_ganhos = ganhos.rolling(14).mean()
    media_perdas = perdas.rolling(14).mean()

    rs = media_ganhos / media_perdas
    rsi = 100 - (100 / (1 + rs))

    preco = float(fechamento.iloc[-1])
    media20 = float(m20.iloc[-1])
    media50 = float(m50.iloc[-1])
    rsi_atual = float(rsi.iloc[-1])

    nota = 50

    if preco > media20:
        nota += 10

    if media20 > media50:
        nota += 10

    if fechamento.iloc[-1] > fechamento.iloc[-6]:
        nota += 10
    else:
        nota -= 10

    if 30 <= rsi_atual <= 70:
        nota += 10
    elif rsi_atual < 30:
        nota += 20
    elif rsi_atual > 70:
        nota -= 10

    nota = max(0, min(100, nota))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💰 Preço", f"R$ {preco:.2f}")
        st.metric("📊 RSI", f"{rsi_atual:.2f}")

    with col2:
        st.metric("📈 Média 20", f"R$ {media20:.2f}")
        st.metric("📉 Média 50", f"R$ {media50:.2f}")

    st.subheader(f"🧠 Nota: {nota}/100")

    if nota >= 70:
        st.success("🟢 SINAL FORTE")
    elif nota >= 50:
        st.warning("🟡 SINAL NEUTRO")
    else:
        st.error("🔴 SINAL FRACO")

st.caption("⚠️ Projeto educacional de simulação. Não é recomendação financeira.")

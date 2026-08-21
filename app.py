import streamlit as st
import pandas as pd
from src.storage import load_state
from src.ui import inject_styles, render_info_card, radar_figure, goals_bar_chart

st.set_page_config(
    page_title="Extensão FEF Futebol 2s2026", page_icon="⚽", layout="wide"
)
inject_styles()

state = load_state()

st.title("⚽ Extensão FEF Futebol 2s2026")
st.markdown("Acompanhe o desempenho semanal do nosso futebol.")

if not state.jogadores:
    st.warning("Nenhum dado encontrado. Verifique a conexão com a planilha.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["🏠 Geral", "👤 Perfil do Jogador", "⚔️ Comparação"])

with tab1:
    st.subheader("Tabela Geral")
    df_geral = pd.DataFrame([p.to_dict() for p in state.jogadores])
    st.dataframe(df_geral, use_container_width=True, hide_index=True)

    st.plotly_chart(goals_bar_chart(state), use_container_width=True)

with tab2:
    nomes = [p.nome for p in state.jogadores]
    selecionado = st.selectbox("Selecione um jogador", nomes)
    jogador = next((p for p in state.jogadores if p.nome == selecionado), None)

    if jogador:
        cols = st.columns(3)
        with cols[0]:
            render_info_card("Gols", str(jogador.gols))
        with cols[1]:
            render_info_card("Assistências", str(jogador.assistencias))
        with cols[2]:
            render_info_card("Participações em gols", str(jogador.participacoes_gols))

        st.plotly_chart(radar_figure(jogador), use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        j1_nome = st.selectbox("Jogador 1", nomes, key="j1")
    with col2:
        j2_nome = st.selectbox(
            "Jogador 2", nomes, index=1 if len(nomes) > 1 else 0, key="j2"
        )

    j1 = next((p for p in state.jogadores if p.nome == j1_nome), None)
    j2 = next((p for p in state.jogadores if p.nome == j2_nome), None)

    if j1 and j2:
        st.plotly_chart(radar_figure(j1, j2), use_container_width=True)

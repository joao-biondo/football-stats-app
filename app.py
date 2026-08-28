import streamlit as st
import pandas as pd
import time
from src.storage import load_state, register_vote
from src.ui import (
    inject_styles,
    refresh_app_data,
    radar_figure,
    goals_bar_chart,
    goals_vs_assists_scatter,
    goals_vs_assists_per_player,
    most_goals_and_assists,
    player_card,
)

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

tab1, tab2, tab3, tab4 = st.tabs(
    ["🏠 Geral", "👤 Perfil do Jogador", "⚔️ Comparação", "⭐ Vote no melhor da semana"]
)

with tab1:
    st.subheader("Tabela Geral")
    df_geral = pd.DataFrame([p.to_dict() for p in state.jogadores])
    st.dataframe(df_geral.iloc[:, :-1], width="stretch", hide_index=True)
    if st.button("🔄 Atualizar Dados"):
        refresh_app_data()
    metrics = most_goals_and_assists(state)
    for idx, col in enumerate(st.columns(3)):
        with col:
            label = list(metrics.keys())[idx]
            for k, v in metrics[label].items():
                player = k
                value = v
            st.metric(
                label,
                value,
                player,
                delta_color="yellow",
                delta_arrow="off",
                border=True,
            )
    st.plotly_chart(goals_bar_chart(state), width="stretch")
    st.plotly_chart(goals_vs_assists_scatter(state), width="stretch")

with tab2:
    nomes = [p.nome for p in state.jogadores]
    selecionado = st.selectbox("Selecione um jogador", nomes)
    jogador = next((p for p in state.jogadores if p.nome == selecionado), None)

    if jogador:
        cols = st.columns(2)
        with cols[0]:
            player_card(jogador)
        with cols[1]:
            st.plotly_chart(radar_figure(jogador), width="stretch")

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        j1_nome = st.selectbox("Jogador 1", nomes, key="j1")
        j1 = next((p for p in state.jogadores if p.nome == j1_nome), None)
        player_card(j1)
    with col2:
        j2_nome = st.selectbox(
            "Jogador 2", nomes, index=1 if len(nomes) > 1 else 0, key="j2"
        )
        j2 = next((p for p in state.jogadores if p.nome == j2_nome), None)
        player_card(j2)

    if j1 and j2:
        st.plotly_chart(radar_figure(j1, j2), width="stretch")
        st.plotly_chart(goals_vs_assists_per_player(j1, j2), width="stretch")

with tab4:
    nomes = [player.nome for player in state.jogadores]
    (
        col1,
        col2,
    ) = st.columns(2)
    with col1:
        st.subheader("Melhor da semana")
        jogador = st.selectbox("Craque:", nomes)
        player_obj = next((p for p in state.jogadores if p.nome == jogador), None)
        if player_obj:
            player_card(player_obj)
        if st.button("Votar", width="stretch", type="primary"):
            res = register_vote(jogador)
            message = res.message
            if res.success:
                st.success(message)
                time.sleep(2)
                refresh_app_data()
            else:
                st.warning(message)
    with col2:
        st.subheader("Ranking de Votos")
        votos = df_geral.sort_values(by="Votos", ascending=False)
        votos = votos.loc[:, ["Jogador", "Votos"]]
        st.table(votos, hide_index=True, height=425)

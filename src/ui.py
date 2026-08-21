import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from .models import AppState, Player


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --pitch-dark: #041e15;
            --pitch-mid: #0a3022;
            --line: rgba(255,255,255,0.1);
            --text: #f0fdf4;
            --muted: rgba(240,253,244,0.7);
            --accent: #006437; 
        }
        .stApp {
            background: linear-gradient(180deg, var(--pitch-dark) 0%, #062319 100%);
            color: var(--text);
        }
        .stat-card {
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 1rem;
            background: rgba(255,255,255,0.03);
            text-align: center;
        }
        .stat-card .label { color: var(--muted); font-size: 0.85rem; text-transform: uppercase; }
        .stat-card .value { color: white; font-size: 1.8rem; font-weight: bold; margin-top: 0.5rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def radar_figure(player_a: Player, player_b: Player = None) -> go.Figure:
    labels = ["Partidas", "Vitórias", "Gols", "Assistências", "Participações"]

    def get_values(p: Player):
        return [p.partidas, p.vitorias, p.gols, p.assistencias, p.participacoes_gols]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=get_values(player_a) + [get_values(player_a)[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=player_a.nome,
            line=dict(color=player_a.cor_tema, width=3),
            hovertemplate="<b>%{theta}</b>: %{r}<extra></extra>",
        )
    )

    if player_b:
        fig.add_trace(
            go.Scatterpolar(
                r=get_values(player_b) + [get_values(player_b)[0]],
                theta=labels + [labels[0]],
                fill="toself",
                name=player_b.nome,
                line=dict(color="#f7c948", width=3),
                hovertemplate="<b>%{theta}</b>: %{r}<extra></extra>",
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.1)")),
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=400,
        margin=dict(l=30, r=30, t=30, b=30),
    )
    return fig


def goals_bar_chart(state: AppState) -> go.Figure:
    df = pd.DataFrame([p.to_dict() for p in state.jogadores])
    if df.empty:
        return go.Figure()

    df = df.sort_values("Participações", ascending=False)
    fig = px.bar(
        df,
        x="Jogador",
        y=["Gols", "Assistências"],
        title="Gols e Assistências por Jogador",
        barmode="stack",
        color_discrete_sequence=["#51cf66", "#4dabf7"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend_title="Métrica",
    )
    return fig

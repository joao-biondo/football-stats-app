import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import random
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
        .player-fut-card {
            background: linear-gradient(135deg, rgba(10, 48, 34, 0.9) 0%, rgba(4, 30, 21, 0.95) 100%);
            border: 2px solid #f7c948;
            border-radius: 20px;
            padding: 1.2rem;
            max-width: 340px;
            margin: 0.5rem auto;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(247, 201, 72, 0.15);
            transition: transform 0.2s ease;
        }

        .player-fut-card:hover {
            transform: translateY(-4px);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 0.8rem;
        }

        .photo-wrapper img {
            width: 75px;
            height: 75px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #f7c948;
            background-color: #062319;
        }

        .player-title h3 {
            margin: 0;
            color: #ffffff;
            font-size: 1.3rem;
            font-weight: 800;
            letter-spacing: 0.5px;
        }

        .badge-winrate {
            display: inline-block;
            background: rgba(247, 201, 72, 0.15);
            color: #f7c948;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 12px;
            margin-top: 4px;
            border: 1px solid rgba(247, 201, 72, 0.3);
        }

        .card-stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
        }

        .stat-box {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 0.5rem;
            text-align: center;
        }

        .stat-box.highlight {
            grid-column: span 2;
            background: linear-gradient(90deg, rgba(247, 201, 72, 0.1), rgba(81, 207, 102, 0.1));
            border: 1px solid rgba(247, 201, 72, 0.3);
        }

        .stat-value {
            display: block;
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 800;
            line-height: 1.2;
        }

        .stat-label {
            display: block;
            color: rgba(240, 253, 244, 0.6);
            font-size: 0.65rem;
            font-weight: 700;
            margin-top: 2px;
            letter-spacing: 0.5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def random_hex_color():
    def f():
        return random.randint(0, 255)

    return "#%02X%02X%02X" % (f(), f(), f())


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
    labels = ["Gols", "Assistências", "Participações"]

    def get_values(p: Player):
        return [p.gols, p.assistencias, p.participacoes_gols]

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
                line=dict(color=player_b.cor_tema, width=3),
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


def goals_vs_assists_scatter(state: AppState) -> go.Figure:
    df = pd.DataFrame([p.to_dict() for p in state.jogadores])
    if df.empty:
        return go.Figure()

    color_map = {p.nome: p.cor_tema for p in state.jogadores}

    fig = px.scatter(
        df,
        x="Assistências",
        y="Gols",
        size="Participações",
        color="Jogador",
        color_discrete_map=color_map,
        hover_name="Jogador",
        size_max=40,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis_title="Assistências",
        yaxis_title="Gols",
        showlegend=True,
    )
    # Add subtle grid lines for readability
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.1)")

    return fig


def goals_vs_assists_per_player(player_a: Player, player_b: Player = None) -> go.Figure:
    if not all([player_a, player_b]):
        return go.Figure()
    df = pd.DataFrame([player_a.to_dict(), player_b.to_dict()])
    fig = px.scatter(
        df,
        x="Assistências",
        y="Gols",
        size="Participações",
        color="Jogador",
        hover_name="Jogador",
        size_max=40,
    )

    return fig


def most_goals_and_assists(state: AppState) -> dict:
    df = pd.DataFrame([p.to_dict() for p in state.jogadores])
    goals = df.iloc[:, 1]
    assists = df.iloc[:, 2]
    involvement = df.iloc[:, 3]
    labels = ["Artilheiro", "Mais Asistências", "Mais Participações"]
    metrics = dict()
    for series, label in zip([goals, assists, involvement], labels):
        idx = series.idxmax()
        player = df.iloc[:, 0][idx]
        metrics[f"{label}"] = {f"{player}": series[idx]}
    return metrics


def player_card(player: Player):
    if not isinstance(player, Player):
        raise TypeError("'player' argument must be an instance of `Player` class.")

    card_html = f"""
    <div class="player-fut-card">
        <div class="card-header">
            <div class="photo-wrapper">
                <img src="{player.foto_url}" alt="{player.nome}" onerror="this.src='https://cdn-icons-png.flaticon.com/512/166/166344.png'"/>
            </div>
            <div class="player-title">
                <h3>{player.nome}</h3>
            </div>
        </div>
        <div class="card-stats-grid">
            <div class="stat-box">
                <span class="stat-value">{player.gols}</span>
                <span class="stat-label">GOLS</span>
            </div>
            <div class="stat-box">
                <span class="stat-value">{player.assistencias}</span>
                <span class="stat-label">ASSISTÊNCIAS</span>
            </div>
            <div class="stat-box">
                <span class="stat-value">{player.participacoes_gols}</span>
                <span class="stat-label">PARTICIPAÇÕES</span>
            </div>
            <div class="stat-box highlight">
                <span class="stat-value">⭐ {player.melhor_da_partida}</span>
                <span class="stat-label">CRAQUE</span>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

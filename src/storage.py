import streamlit as st
from streamlit_gsheets import GSheetsConnection
from .models import Player, AppState


@st.cache_resource
def _get_gsheets_connection() -> GSheetsConnection:
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as exc:
        raise RuntimeError(
            "Falha ao inicializar GSheetsConnection. Verifique as configurações."
        ) from exc


@st.cache_data(ttl=300)
def load_state() -> AppState:
    try:
        conn = _get_gsheets_connection()
        df = conn.read()

        if df is None or df.empty:
            return AppState()

        jogadores = []
        for _, row in df.iterrows():
            nome = str(row.get("Player", "")).strip()
            if not nome or nome.lower() == "nan":
                continue

            jogador = Player(
                nome=nome,
                partidas=int(row.get("Matches", 0) or 0),
                vitorias=int(row.get("Wins", 0) or 0),
                empates=int(row.get("Draw", 0) or 0),
                derrotas=int(row.get("Losses", 0) or 0),
                gols=int(row.get("Goals", 0) or 0),
                assistencias=int(row.get("Assists", 0) or 0),
                foto_url=str(row.get("Foto", "")).strip(),
            )
            jogadores.append(jogador)

        return AppState(jogadores=jogadores)
    except Exception as exc:
        st.error(f"Erro ao carregar dados: {exc}")
        return AppState()

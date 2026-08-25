import streamlit as st
from streamlit_gsheets import GSheetsConnection
from .models import Player, AppState
from typing import NamedTuple
import uuid
import requests


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
        df = df.replace(float("NaN"), 0)

        if df is None or df.empty:
            return AppState()

        jogadores = []
        for _, row in df.iterrows():
            nome = str(row.get("Player", "")).strip()
            if not nome or nome.lower() == "nan":
                continue

            jogador = Player(
                nome=nome,
                gols=int(row.get("Goals", 0) or 0),
                assistencias=int(row.get("Assists", 0) or 0),
                melhor_da_partida=int(row.get("Man of the Match", 0) or 0),
                foto_url=str(row.get("Foto", "")).strip(),
            )
            jogadores.append(jogador)

        return AppState(jogadores=jogadores)
    except Exception as exc:
        st.error(f"Erro ao carregar dados: {exc}")
        return AppState()


def _get_voter_id():
    if "voter_id" not in st.session_state:
        st.session_state.voter_id = str(uuid.uuid4())[:8]
    return st.session_state.voter_id


class TableRequestResponse(NamedTuple):
    success: bool
    message: str


def register_vote(player: str) -> TableRequestResponse:
    try:
        url = st.secrets.get("connections").get("voting_url").get("url")
    except (KeyError, AttributeError):
        return TableRequestResponse(
            success=False,
            message="Key 'url' not found at .streamlit/secrets.toml! Please, verify the deployment (see README for instructions).",
        )

    try:
        payload = {"jogador": player, "voter_id": _get_voter_id()}
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        success = data.get("status") == "success"
        message = data.get("message")

        return TableRequestResponse(success=success, message=message)

    except requests.exceptions.Timeout:
        return TableRequestResponse(
            success=False,
            message="O Google Apps Script demorou muito para responder (Timeout). Tente novamente.",
        )
    except requests.exceptions.ConnectionError:
        return TableRequestResponse(
            success=False, message="Falha de conexão. Verifique sua conexão de rede."
        )
    except requests.exceptions.HTTPError as http_err:
        return TableRequestResponse(
            success=False, message=f"Erro HTTP no servidor: {http_err}"
        )
    except requests.exceptions.RequestException as err:
        return TableRequestResponse(
            success=False, message=f"Erro inesperado na requisição: {err}"
        )

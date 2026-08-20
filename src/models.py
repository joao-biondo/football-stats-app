from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(slots=True)
class Player:
    nome: str
    partidas: int = 0
    vitorias: int = 0
    empates: int = 0
    derrotas: int = 0
    gols: int = 0
    assistencias: int = 0
    foto_url: str = ""
    cor_tema: str = "#006437"  # Verde clássico como padrão

    @property
    def participacoes_gols(self) -> int:
        return self.gols + self.assistencias

    @property
    def aproveitamento(self) -> float:
        if self.partidas == 0:
            return 0.0
        pontos_ganhos = (self.vitorias * 3) + self.empates
        pontos_totais = self.partidas * 3
        return (pontos_ganhos / pontos_totais) * 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Jogador": self.nome,
            "Partidas": self.partidas,
            "Vitórias": self.vitorias,
            "Empates": self.empates,
            "Derrotas": self.derrotas,
            "Gols": self.gols,
            "Assistências": self.assistencias,
            "Participações": self.participacoes_gols,
            "Aproveitamento (%)": round(self.aproveitamento, 1),
        }


@dataclass(slots=True)
class AppState:
    jogadores: list[Player] = field(default_factory=list)

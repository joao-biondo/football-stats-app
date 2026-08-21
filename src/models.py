from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(slots=True)
class Player:
    nome: str
    gols: int = 0
    assistencias: int = 0
    foto_url: str = ""
    cor_tema: str = "#006437"  # Verde clássico como padrão

    @property
    def participacoes_gols(self) -> int:
        return self.gols + self.assistencias

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Jogador": self.nome,
            "Gols": self.gols,
            "Assistências": self.assistencias,
            "Participações": self.participacoes_gols,
        }


@dataclass(slots=True)
class AppState:
    jogadores: list[Player] = field(default_factory=list)

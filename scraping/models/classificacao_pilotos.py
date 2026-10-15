from dataclasses import dataclass, field
from .piloto import Piloto

@dataclass
class ClassificacaoPilotos():
    titulo:str
    pilotos_list:list[Piloto] = field(init=False, default_factory=list)

    def inserir_piloto(self, piloto:Piloto) -> None:
        self.pilotos_list.append(piloto)

    def get_pilotos_list(self) -> list[Piloto]:
        return sorted(self.pilotos_list, key=lambda piloto: piloto.colocacao)

    def __str__(self):
        classificacao_list = [f"{self.titulo:^61}\n\n"]
        pilotos_list_sorted = sorted(self.pilotos_list, key=lambda piloto: piloto.colocacao)

        for pilotos in pilotos_list_sorted:
            classificacao_list.append(f"{str(pilotos)}\n")

        return "".join(classificacao_list)
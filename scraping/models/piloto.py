from dataclasses import dataclass

@dataclass
class Piloto():
    nome:str
    pais:str
    equipe:str
    pontos:int
    colocacao:int

    def __str__(self):
        return f"| {self.colocacao} - {f'{self.nome} ({self.pais})':<35} \t |  {f'{self.pontos:<4} pts':<9} |"
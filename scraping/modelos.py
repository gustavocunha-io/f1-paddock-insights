from dataclasses import dataclass, field
from typing import List


@dataclass
class Piloto():
    nome:str
    escuderia:str
    pais:str

@dataclass
class EstatisticaPiloto():
    piloto:Piloto
    pontos:int
    posicao:int

@dataclass
class Classificacao():
    titulo:str
    tabela:List[EstatisticaPiloto] = field(default=list)
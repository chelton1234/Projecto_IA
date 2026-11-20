# core/__init__.py
# Este ficheiro torna a pasta 'core' um módulo Python

from .responder_mocambique import ResponderMocambique
from .buscador_mocambique import BuscadorMocambique
from .gerenciador_conteudo import GerenciadorConteudo

__all__ = [
    'ResponderMocambique',
    'BuscadorMocambique', 
    'GerenciadorConteudo'
]
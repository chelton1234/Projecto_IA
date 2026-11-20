# core/agentes/agente_busca.py
# Agente de busca em sites oficiais - SEM IA, apenas extração

import time
from .base_agente import BaseAgente

class AgenteBusca(BaseAgente):
    """Agente que busca em sites oficiais moçambicanos"""
    
    def __init__(self, buscador):
        super().__init__("🔍 Agente de Busca", prioridade=2, tipo="oficial")
        self.buscador = buscador
        self.cache = {}
    
    def pode_processar(self, pergunta):
        """Perguntas que precisam de dados específicos"""
        palavras = ['quantos', 'quantas', 'valor', 'taxa', 'dados', 
                   'estatística', 'inflação', 'pib', 'população',
                   'médicos', 'hospitais', 'escolas', 'universidades',
                   'preço', 'custo', 'número', 'numero']
        pergunta_lower = pergunta.lower()
        return any(p in pergunta_lower for p in palavras)
    
    def processar(self, pergunta):
        """Busca em sites oficiais e extrai resposta"""
        inicio = time.time()
        
        # Verificar cache
        if pergunta in self.cache:
            return self.cache[pergunta]
        
        # Buscar resposta exata
        resultado = self.buscador.buscar_resposta_exata(pergunta)
        
        self.registrar_consulta(time.time() - inicio)
        
        if resultado:
            self.registrar_resposta()
            resposta = self.buscador.formatar_resposta(resultado)
            self.cache[pergunta] = resposta
            return resposta
        
        return None
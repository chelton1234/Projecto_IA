# core/agentes/agente_local.py
# Agente de fatos imutáveis (base local) - SEM IA

import time
from .base_agente import BaseAgente

class AgenteLocal(BaseAgente):
    """Agente para fatos imutáveis - respostas rápidas sem IA"""
    
    def __init__(self, gerenciador):
        super().__init__("📚 Agente Local", prioridade=1, tipo="local")
        self.gerenciador = gerenciador
        
        # Fatos imutáveis (nunca mudam)
        self.fatos = {
            "capital": "A capital de Moçambique é Maputo.",
            "presidente": "O Presidente de Moçambique é Daniel Chapo (2025-presente).",
            "moeda": "A moeda oficial de Moçambique é o Metical (MZN).",
            "lingua_oficial": "A língua oficial de Moçambique é o Português.",
            "independencia": "A independência de Moçambique foi a 25 de junho de 1975.",
            "provincias": "Moçambique tem 11 províncias: Maputo Cidade, Maputo Província, Gaza, Inhambane, Manica, Sofala, Tete, Zambézia, Nampula, Niassa, Cabo Delgado."
        }
    
    def pode_processar(self, pergunta):
        """Perguntas sobre fatos básicos"""
        palavras = ['capital', 'presidente', 'moeda', 'língua', 'lingua', 
                   'independência', 'independencia', 'províncias', 'provincias']
        pergunta_lower = pergunta.lower()
        return any(p in pergunta_lower for p in palavras)
    
    def processar(self, pergunta):
        """Resposta baseada em fatos locais"""
        inicio = time.time()
        pergunta_lower = pergunta.lower()
        
        resposta = None
        if 'capital' in pergunta_lower:
            resposta = self.fatos['capital']
        elif 'presidente' in pergunta_lower:
            resposta = self.fatos['presidente']
        elif 'moeda' in pergunta_lower:
            resposta = self.fatos['moeda']
        elif 'língua' in pergunta_lower or 'lingua' in pergunta_lower:
            resposta = self.fatos['lingua_oficial']
        elif 'independência' in pergunta_lower or 'independencia' in pergunta_lower:
            resposta = self.fatos['independencia']
        elif 'províncias' in pergunta_lower or 'provincias' in pergunta_lower:
            resposta = self.fatos['provincias']
        else:
            # Tentar base de conhecimento local
            resposta = self.gerenciador.buscar_local(pergunta)
        
        self.registrar_consulta(time.time() - inicio)
        
        if resposta:
            self.registrar_resposta()
            return f"📚 **Fonte: Base de Conhecimento Local**\n\n{resposta}"
        
        return None
# core/agentes/sociedade.py
# Sociedade de Agentes - Google First!

import time
from .agente_grounding import AgenteGrounding
from .agente_busca import AgenteBusca
from .agente_local import AgenteLocal

class SociedadeAgentes:
    """Coordena os agentes - PRIORIDADE: Google Search primeiro"""

    MODOS = {
        "local": ["local"],
        "web": ["web", "local"],
        "hibrido": ["web", "oficial", "local"]
    }

    def __init__(self, gerenciador, buscador, api_key=None):
        self.agentes = []
        
        # PRIORIDADE 1: Google Search (Grounding) - RESPOSTAS REAIS DA WEB
        if api_key:
            self.agentes.append(AgenteGrounding(api_key))
        
        # PRIORIDADE 2: Busca em sites oficiais (fallback)
        self.agentes.append(AgenteBusca(buscador))
        
        # PRIORIDADE 3: Base local (último recurso)
        self.agentes.append(AgenteLocal(gerenciador))
        
        self.estatisticas = {
            "total_perguntas": 0,
            "agente_vencedor": {},
            "tempo_total": 0
        }
    
    def processar_pergunta(self, pergunta, modo="hibrido"):
        """Processa pergunta - PRIORIDADE: Google Search primeiro"""
        inicio = time.time()

        tipos = self.MODOS.get(modo, self.MODOS["hibrido"])
        agentes = [a for a in self.agentes if a.tipo in tipos]

        print(f"\n🔍 Processando pergunta ({modo}): {pergunta[:50]}...")

        for agente in agentes:
            print(f"  → Tentando: {agente.nome}")
            
            resposta = agente.processar(pergunta)
            
            if resposta:
                tempo = time.time() - inicio
                print(f"  ✅ Resposta de: {agente.nome} ({tempo:.2f}s)")
                
                self.estatisticas["total_perguntas"] += 1
                self.estatisticas["agente_vencedor"][agente.nome] = \
                    self.estatisticas["agente_vencedor"].get(agente.nome, 0) + 1
                self.estatisticas["tempo_total"] += tempo
                
                return resposta
        
        print("  ❌ Nenhuma resposta encontrada")
        return None
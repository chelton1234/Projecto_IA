# core/agentes/base_agente.py
# Classe base para todos os agentes

from abc import ABC, abstractmethod

class BaseAgente(ABC):
    """Classe base para todos os agentes da sociedade"""
    
    def __init__(self, nome, prioridade=5, tipo="geral"):
        self.nome = nome
        self.prioridade = prioridade  # 1=mais alta, 10=mais baixa
        self.tipo = tipo
        self.total_consultas = 0
        self.total_respostas = 0
        self.tempo_total = 0
    
    @abstractmethod
    def pode_processar(self, pergunta):
        """Verifica se este agente pode processar a pergunta"""
        pass
    
    @abstractmethod
    def processar(self, pergunta):
        """Processa a pergunta e retorna resposta"""
        pass
    
    def registrar_consulta(self, tempo):
        """Registra estatísticas da consulta"""
        self.total_consultas += 1
        self.tempo_total += tempo
    
    def registrar_resposta(self):
        """Registra que o agente respondeu"""
        self.total_respostas += 1
    
    def get_status(self):
        """Retorna status do agente"""
        tempo_medio = self.tempo_total / max(1, self.total_consultas)
        return {
            "nome": self.nome,
            "prioridade": self.prioridade,
            "consultas": self.total_consultas,
            "respostas": self.total_respostas,
            "tempo_medio": f"{tempo_medio:.2f}s"
        }
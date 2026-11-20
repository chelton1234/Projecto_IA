# utils/formatador.py
# Funções de formatação de texto

import re
from datetime import datetime

class FormatadorTexto:
    """Classe com funções de formatação de texto"""
    
    @staticmethod
    def limpar_texto(texto):
        """Limpa e normaliza texto"""
        texto = re.sub(r'\s+', ' ', texto)
        texto = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)]', '', texto)
        return texto.strip()
    
    @staticmethod
    def resumir_texto(texto, max_caracteres=300):
        """Resume texto para preview"""
        if len(texto) <= max_caracteres:
            return texto
        return texto[:max_caracteres] + "..."
    
    @staticmethod
    def formatar_data(data):
        """Formata data para exibição"""
        if isinstance(data, datetime):
            return data.strftime("%d/%m/%Y")
        return str(data)
    
    @staticmethod
    def formatar_numero(numero):
        """Formata número com separadores"""
        try:
            return f"{int(numero):,}".replace(",", ".")
        except:
            return str(numero)
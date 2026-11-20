# core/filtro_contexto.py
# Filtro para garantir que só responde sobre Moçambique

import re

class FiltroContexto:
    """Filtra perguntas para permitir apenas sobre Moçambique"""
    
    # Palavras-chave relacionadas a Moçambique
    PALAVRAS_MOCAMBIQUE = [
        'moçambique', 'mocambique', 'moçambicano', 'mocambicana',
        'maputo', 'beira', 'nampula', 'matola', 'chimoio', 'tete',
        'quelimane', 'xai-xai', 'inhambane', 'lichinga', 'pemba',
        'zambeze', 'limpopo', 'save', 'rovuma',
        'gorongosa', 'bazaruto', 'quirimbas', 'tofo', 'vilanculos',
        'ine', 'banco de moçambique', 'portaldogoverno', 'tvm', 'rm',
        'presidente', 'daniel chapo', 'frelimo', 'renamo', 'mdm'
    ]
    
    # Países para bloquear explicitamente
    PAISES_BLOQUEADOS = [
        'brasil', 'brasileiro', 'portugal', 'angola', 'cabo verde',
        'são tomé', 'guiné-bissau', 'timor', 'timor leste', 'china', 'estados unidos',
        'eua', 'inglaterra', 'reino unido', 'frança', 'alemanha', 'espanha',
        'italia', 'rússia', 'japão', 'coreia', 'india', 'argentina', 'mexico'
    ]
    
    # Categorias permitidas
    CATEGORIAS_PERMITIDAS = [
        'cultura', 'turismo', 'economia', 'politica', 'saude', 'educacao',
        'geografia', 'historia', 'desporto', 'tecnologia', 'governo'
    ]
    
    def __init__(self):
        self.estatisticas = {
            "perguntas_aceites": 0,
            "perguntas_bloqueadas": 0,
            "ultimo_bloqueio": None
        }
    
    def _contem_palavra_mocambique(self, texto):
        """Verifica se o texto contém referência a Moçambique"""
        texto_lower = texto.lower()
        
        for palavra in self.PALAVRAS_MOCAMBIQUE:
            if palavra in texto_lower:
                return True
        return False
    
    def _menciona_outro_pais(self, texto):
        """Verifica se o texto menciona outro país explicitamente"""
        texto_lower = texto.lower()
        
        for pais in self.PAISES_BLOQUEADOS:
            if pais in texto_lower:
                return True
        return False
    
    def _is_pergunta_geral(self, texto):
        """Verifica se é uma pergunta muito geral que pode ser sobre Moçambique"""
        perguntas_gerais = [
            'qual é a capital', 'quem é o presidente', 'qual é a moeda',
            'qual a população', 'quantas províncias', 'fale sobre',
            'explique', 'o que é', 'como funciona', 'quais são'
        ]
        
        texto_lower = texto.lower()
        for pergunta in perguntas_gerais:
            if texto_lower.startswith(pergunta) or pergunta in texto_lower:
                return True
        return False
    
    def _extrair_contexto(self, texto):
        """Tenta extrair contexto geográfico da pergunta"""
        texto_lower = texto.lower()
        
        # Se mencionar explicitamente Moçambique
        if 'moçambique' in texto_lower or 'mocambique' in texto_lower:
            return 'mocambique'
        
        # Se mencionar cidade/província moçambicana
        for palavra in self.PALAVRAS_MOCAMBIQUE:
            if palavra in texto_lower:
                return 'mocambique'
        
        return None
    
    def validar(self, pergunta):
        """
        Valida se a pergunta é sobre Moçambique
        Retorna: (aceite, mensagem_erro)
        """
        pergunta_lower = pergunta.lower()
        
        # Caso 1: Pergunta vazia
        if not pergunta.strip():
            return False, "Por favor, digite uma pergunta."
        
        assunto_lingua = any(p in pergunta_lower for p in ('língua', 'lingua', 'idioma'))
        if (self._menciona_outro_pais(pergunta_lower)
                and not self._contem_palavra_mocambique(pergunta_lower)
                and not assunto_lingua):
            self.estatisticas["perguntas_bloqueadas"] += 1
            self.estatisticas["ultimo_bloqueio"] = pergunta
            return False, self._mensagem_bloqueio(pergunta)

        self.estatisticas["perguntas_aceites"] += 1
        return True, None
    
    def _mensagem_bloqueio(self, pergunta):
        """Mensagem quando a pergunta é bloqueada"""
        return f"""🇲🇿 **Desculpe, não posso responder a essa pergunta.**

Sou um assistente especializado **apenas em Moçambique**.

✅ **Posso ajudar com:**
• Informações sobre Moçambique (cultura, turismo, economia)
• Dados oficiais do governo moçambicano
• Estatísticas do INE e Banco de Moçambique
• Notícias e atualidades de Moçambique

❓ **Tente perguntar sobre:**
• "Qual é a capital de Moçambique?"
• "Como é a cultura moçambicana?"
• "Quais são as praias de Moçambique?"
• "Dados da economia moçambicana"

💡 Se a sua pergunta é sobre Moçambique, tente incluir o nome do país.
"""
    
    def _mensagem_ajuda(self):
        """Mensagem de ajuda para perguntas ambíguas"""
        return f"""🇲🇿 **Não consegui identificar se a sua pergunta é sobre Moçambique.**

Sou um assistente especializado **apenas em Moçambique**.

💡 **Para obter respostas, pergunte sobre:**
• Geografia: capital, províncias, rios, clima
• Cultura: gastronomia, música, dança, tradições
• Turismo: praias, parques nacionais, cidades históricas
• Economia: moeda, PIB, principais produtos
• Política: presidente, governadores, partidos
• Dados oficiais: população, saúde, educação

📝 **Exemplos:**
• "Qual é a capital de Moçambique?"
• "Fale sobre a cultura moçambicana"
• "Quais são as praias mais bonitas?"

🔍 Se for sobre Moçambique, mencione o país na pergunta.
"""
    
    def get_estatisticas(self):
        """Retorna estatísticas do filtro"""
        total = self.estatisticas["perguntas_aceites"] + self.estatisticas["perguntas_bloqueadas"]
        return {
            "aceites": self.estatisticas["perguntas_aceites"],
            "bloqueadas": self.estatisticas["perguntas_bloqueadas"],
            "taxa_aceitacao": round(self.estatisticas["perguntas_aceites"] / max(1, total) * 100, 1)
        }
# core/agentes/agente_grounding.py
# Agente que busca na Google - Mostra apenas fontes governamentais

import time
import re
from .base_agente import BaseAgente

class AgenteGrounding(BaseAgente):
    """Agente que pesquisa na Google - Filtra apenas fontes governamentais"""
    
    def __init__(self, api_key):
        super().__init__("🔎 Google Search", prioridade=1, tipo="web")
        self.api_key = api_key
        self.disponivel = self._verificar_disponibilidade()
        
        if self.disponivel:
            print("✅ Google Search ativado - respostas em tempo real")
    
    def _verificar_disponibilidade(self):
        try:
            from google import genai
            return bool(self.api_key)
        except ImportError:
            return False
    
    def _filtrar_fontes_governamentais(self, texto):
        """Extrai apenas fontes .gov.mz do texto"""
        if not texto:
            return ""
        
        # Procurar por URLs com .gov.mz
        padrao_gov = r'https?://[^\s]+\.gov\.mz[^\s]*'
        fontes_gov = re.findall(padrao_gov, texto)
        
        # Procurar também por domínios conhecidos
        dominios_confiaveis = [
            'ine.gov.mz', 'bancomoc.mz', 'portaldogoverno.gov.mz',
            'presidente.gov.mz', 'parlamento.mz', 'misau.gov.mz',
            'mined.gov.mz', 'mef.gov.mz'
        ]
        
        fontes_extra = []
        for dominio in dominios_confiaveis:
            padrao = rf'https?://[^\s]*{re.escape(dominio)}[^\s]*'
            encontradas = re.findall(padrao, texto)
            fontes_extra.extend(encontradas)
        
        todas_fontes = list(set(fontes_gov + fontes_extra))
        
        if todas_fontes:
            # Formatar fontes de forma amigável
            resultado = "\n\n📚 **Fontes oficiais Moçambique:**\n"
            for fonte in todas_fontes[:3]:  # Limitar a 3 fontes
                # Extrair nome do domínio
                nome = fonte.replace('https://', '').replace('http://', '').split('/')[0]
                resultado += f"   • {nome}\n"
            return resultado
        
        return ""  # Sem fontes governamentais, não mostra nada
    
    def pode_processar(self, pergunta):
        return True
    
    def processar(self, pergunta):
        """Busca na Google em tempo real - apenas fontes governamentais"""
        if not self.disponivel:
            return None
        
        inicio = time.time()
        
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=self.api_key)
            
            # Prompt que prioriza fontes governamentais
            prompt = f"""
            És o MozAssist Pro, assistente especializado em Moçambique.
            Pesquise na Google e responda a seguinte pergunta no contexto de Moçambique: {pergunta}

            PRIORIZE fontes oficiais moçambicanas (.gov.mz, ine.gov.mz, bancomoc.mz).
            Responda em português de forma clara e directa.
            Se possível, cite informações destas fontes.
            """
            
            grounding_tool = types.Tool(google_search=types.GoogleSearch())
            
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[grounding_tool]
                )
            )
            
            self.registrar_consulta(time.time() - inicio)
            
            if not response or not getattr(response, "text", None):
                return None

            resposta_texto = response.text.strip()
            if not resposta_texto or resposta_texto.lower().startswith(("erro", "error")):
                return None

            self.registrar_resposta()

            # Extrair apenas fontes governamentais
            fontes_gov = self._filtrar_fontes_governamentais(resposta_texto)

            # Limpar o texto de links longos
            resposta_limpa = re.sub(r'🔗 Fonte: https?://vertexaisearch\.cloud\.google\.com[^\s]+', '', resposta_texto)
            resposta_limpa = re.sub(r'https?://vertexaisearch\.cloud\.google\.com[^\s]+', '', resposta_limpa)
            resposta_limpa = re.sub(r'\n{3,}', '\n\n', resposta_limpa)

            return f"""🔍 **Resposta da Pesquisa Google**

📝 **{pergunta}**

{resposta_limpa}
{fontes_gov}


"""

        except Exception as e:
            print(f"❌ Erro no Google Search: {e}")
            return None
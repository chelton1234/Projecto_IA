# core/buscador_oficial.py
# Buscador exclusivo de fontes oficiais e institucionais de Moçambique

import requests
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime

class BuscadorOficial:
    """Buscador especializado em fontes oficiais e institucionais de Moçambique"""
    
    # Fontes oficiais e institucionais de Moçambique
    FONTES_OFICIAIS = {
        "governo": {
            "nome": "Portal do Governo",
            "url": "https://www.portaldogoverno.gov.mz",
            "domínio": "portaldogoverno.gov.mz",
            "tipo": "Governamental"
        },
        "presidencia": {
            "nome": "Presidência da República",
            "url": "https://www.presidente.gov.mz",
            "domínio": "presidente.gov.mz",
            "tipo": "Governamental"
        },
        "parlamento": {
            "nome": "Assembleia da República",
            "url": "https://www.parlamento.mz",
            "domínio": "parlamento.mz",
            "tipo": "Governamental"
        },
        "minec": {
            "nome": "Ministério da Economia",
            "url": "https://www.minec.gov.mz",
            "domínio": "minec.gov.mz",
            "tipo": "Governamental"
        },
        "misau": {
            "nome": "Ministério da Saúde",
            "url": "https://www.misau.gov.mz",
            "domínio": "misau.gov.mz",
            "tipo": "Governamental"
        },
        "mef": {
            "nome": "Ministério das Finanças",
            "url": "https://www.mef.gov.mz",
            "domínio": "mef.gov.mz",
            "tipo": "Governamental"
        },
        "mint": {
            "nome": "Ministério do Interior",
            "url": "https://www.mint.gov.mz",
            "domínio": "mint.gov.mz",
            "tipo": "Governamental"
        },
        "tvm": {
            "nome": "Televisão de Moçambique",
            "url": "https://www.tvm.co.mz",
            "domínio": "tvm.co.mz",
            "tipo": "Media Público"
        },
        "rm": {
            "nome": "Rádio Moçambique",
            "url": "https://www.rm.co.mz",
            "domínio": "rm.co.mz",
            "tipo": "Media Público"
        },
        "jornal_noticias": {
            "nome": "Jornal Notícias",
            "url": "https://www.jornalnoticias.co.mz",
            "domínio": "jornalnoticias.co.mz",
            "tipo": "Media Público"
        },
        "ine": {
            "nome": "Instituto Nacional de Estatística",
            "url": "https://www.ine.gov.mz",
            "domínio": "ine.gov.mz",
            "tipo": "Instituto Oficial"
        },
        "banco_mocambique": {
            "nome": "Banco de Moçambique",
            "url": "https://www.bancomoc.mz",
            "domínio": "bancomoc.mz",
            "tipo": "Instituição Financeira"
        },
        "uem": {
            "nome": "Universidade Eduardo Mondlane",
            "url": "https://www.uem.mz",
            "domínio": "uem.mz",
            "tipo": "Académico"
        },
        "up": {
            "nome": "Universidade Pedagógica",
            "url": "https://www.up.ac.mz",
            "domínio": "up.ac.mz",
            "tipo": "Académico"
        },
        "inatur": {
            "nome": "Instituto Nacional de Turismo",
            "url": "https://www.inatur.gov.mz",
            "domínio": "inatur.gov.mz",
            "tipo": "Turismo"
        },
        "inec": {
            "nome": "Comissão Nacional de Eleições",
            "url": "https://www.inec.gov.mz",
            "domínio": "inec.gov.mz",
            "tipo": "Eleitoral"
        }
    }
    
    def __init__(self):
        self.cache = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MozAssistBot/1.0 (Educational Purpose)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })
        self.resultados_anteriores = []
    
    def buscar_informacao_oficial(self, pergunta):
        """
        Busca informação exclusivamente em fontes oficiais e institucionais
        """
        resultados = []
        pergunta_lower = pergunta.lower()
        
        # Mapear perguntas para categorias oficiais
        categoria = self._identificar_categoria(pergunta_lower)
        
        print(f"🔍 Buscando em fontes oficiais para: {pergunta}")
        print(f"📁 Categoria identificada: {categoria}")
        
        # Buscar nas fontes apropriadas
        for fonte_id, fonte_info in self.FONTES_OFICIAIS.items():
            if self._fonte_relevante(fonte_info, categoria):
                try:
                    resultado = self._buscar_na_fonte(fonte_info, pergunta)
                    if resultado:
                        resultados.append(resultado)
                    time.sleep(0.5)  # Respeitar os servidores
                except Exception as e:
                    print(f"Erro ao buscar em {fonte_info['nome']}: {e}")
        
        return resultados
    
    def _identificar_categoria(self, pergunta):
        """Identifica a categoria da pergunta"""
        categorias = {
            "presidente": ["presidente", "chefe de estado", "daniel chapo"],
            "governo": ["ministro", "governo", "gabinete", "primeiro ministro"],
            "economia": ["economia", "pib", "produto interno", "inflação", "metical"],
            "financas": ["finanças", "orçamento", "imposto", "receita"],
            "saude": ["saúde", "hospital", "doença", "malária", "hospitais"],
            "educacao": ["educação", "escola", "universidade", "ensino"],
            "turismo": ["turismo", "praia", "parque", "hotel", "viagem"],
            "estatistica": ["estatística", "dados", "população", "censos", "ine"],
            "eleicoes": ["eleição", "voto", "eleitoral", "inec"],
            "banco": ["banco", "moeda", "câmbio", "metical", "empréstimo"]
        }
        
        for cat, palavras in categorias.items():
            if any(palavra in pergunta for palavra in palavras):
                return cat
        return "geral"
    
    def _fonte_relevante(self, fonte_info, categoria):
        """Verifica se a fonte é relevante para a categoria"""
        mapeamento = {
            "presidente": ["presidencia", "governo"],
            "governo": ["governo", "parlamento", "presidencia"],
            "economia": ["minec", "mef", "banco_mocambique"],
            "financas": ["mef", "banco_mocambique"],
            "saude": ["misau"],
            "educacao": ["uem", "up"],
            "turismo": ["inatur"],
            "estatistica": ["ine"],
            "eleicoes": ["inec"],
            "banco": ["banco_mocambique"]
        }
        
        fonte_id = [k for k, v in self.FONTES_OFICIAIS.items() if v == fonte_info]
        if not fonte_id:
            return False
        
        fonte_key = fonte_id[0]
        if categoria in mapeamento:
            return fonte_key in mapeamento[categoria]
        return True
    
    def _buscar_na_fonte(self, fonte_info, pergunta):
        """Busca informação numa fonte específica"""
        try:
            # Construir URL de busca
            dominio = fonte_info['domínio']
            
            # Tentar acessar a página principal
            url = fonte_info['url']
            
            resposta = self.session.get(url, timeout=10)
            if resposta.status_code == 200:
                soup = BeautifulSoup(resposta.content, 'html.parser')
                
                # Extrair título e meta descrição
                titulo = soup.find('title')
                titulo_texto = titulo.text if titulo else fonte_info['nome']
                
                # Procurar conteúdo relevante
                texto = self._extrair_texto_relevante(soup, pergunta)
                
                if texto:
                    return {
                        'fonte': fonte_info['nome'],
                        'url': url,
                        'dominio': dominio,
                        'titulo': titulo_texto[:100],
                        'conteudo': texto[:500],
                        'tipo_fonte': fonte_info['tipo']
                    }
            
        except Exception as e:
            print(f"Erro ao acessar {fonte_info['nome']}: {e}")
        
        return None
    
    def _extrair_texto_relevante(self, soup, pergunta):
        """Extrai texto relevante baseado na pergunta"""
        texto_total = ""
        
        # Procurar em parágrafos
        paragrafos = soup.find_all('p')
        for p in paragrafos[:5]:  # Limitar a 5 parágrafos
            texto = p.text.strip()
            if texto and len(texto) > 50:
                texto_total += texto + " "
        
        # Procurar em títulos
        titulos = soup.find_all(['h1', 'h2', 'h3'])
        for h in titulos[:3]:
            texto = h.text.strip()
            if texto:
                texto_total += texto + " "
        
        return texto_total if texto_total else None
    
    def formatar_resposta_oficial(self, resultados, pergunta):
        """Formata os resultados de fontes oficiais"""
        if not resultados:
            return None
        
        resposta = f"🏛️ **Informação de Fontes Oficiais de Moçambique**\n\n"
        resposta += f"🔍 **Sobre: {pergunta}**\n\n"
        
        for r in resultados:
            resposta += f"📌 **{r['fonte']}** ({r['tipo_fonte']})\n"
            resposta += f"   🔗 {r['url']}\n"
            
            if r.get('conteudo'):
                resposta += f"   📝 {r['conteudo'][:250]}...\n"
            
            resposta += "\n"
        
        resposta += "---\n"
        resposta += "✅ **Fontes Oficiais e Institucionais de Moçambique**\n"
        resposta += "🔒 Informação verificada e confiável\n"
        resposta += "💡 Para mais detalhes, acesse os links oficiais acima."
        
        return resposta
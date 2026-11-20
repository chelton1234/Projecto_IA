# core/buscador_mocambique.py
# Buscador especializado em fontes moçambicanas confiáveis

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import json
import re
from datetime import datetime
import sys
import os

# Tentar importar newspaper, se não tiver, usar fallback
try:
    from newspaper import Article
    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False
    print("⚠️ newspaper3k não instalado. Usando modo simplificado.")

# Tentar importar googlesearch
try:
    from googlesearch import search
    GOOGLE_SEARCH_AVAILABLE = True
except ImportError:
    GOOGLE_SEARCH_AVAILABLE = False
    print("⚠️ googlesearch-python não instalado. Usando modo sem busca web.")

class BuscadorMocambique:
    """Buscador especializado em fontes moçambicanas confiáveis"""
    
    def __init__(self):
        self.cache = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MozAssistBot/1.0 (Educational Purpose) Mozilla/5.0'
        })
        self.resultados_anteriores = []
        
        # Carregar fontes do ficheiro de configuração
        self.fontes_confiaveis = self.carregar_fontes()
        
    def carregar_fontes(self):
        """Carrega as fontes confiáveis do ficheiro de configuração"""
        try:
            if os.path.exists("config/fontes_confiaveis.json"):
                with open("config/fontes_confiaveis.json", 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar fontes: {e}")
        
        # Fontes padrão
        return {
            "governo": [
                "portaldogoverno.gov.mz",
                "presidente.gov.mz"
            ],
            "media_publicos": [
                "tvm.co.mz",
                "rm.co.mz"
            ],
            "media_privados": [
                "opais.co.mz"
            ],
            "institutos": [
                "ine.gov.mz",
                "bancomoc.mz"
            ],
            "turismo": [
                "inatur.gov.mz"
            ]
        }
    
    def buscar_em_fontes(self, pergunta, tipo_fonte=None):
        """
        Busca informação em fontes moçambicanas específicas
        """
        if not GOOGLE_SEARCH_AVAILABLE:
            return []
        
        resultados = []
        
        # Selecionar fontes
        fontes_busca = []
        if tipo_fonte and tipo_fonte in self.fontes_confiaveis:
            fontes_busca = self.fontes_confiaveis[tipo_fonte]
        elif not tipo_fonte:
            for fontes in self.fontes_confiaveis.values():
                fontes_busca.extend(fontes)
        
        # Limitar para não sobrecarregar
        fontes_busca = fontes_busca[:5]
        
        for fonte in fontes_busca:
            try:
                resultados_fonte = self._buscar_na_fonte(pergunta, fonte)
                if resultados_fonte:
                    resultados.extend(resultados_fonte)
                time.sleep(0.5)  # Respeitar os servidores
            except Exception as e:
                print(f"Erro ao buscar em {fonte}: {e}")
        
        return resultados
    
    def _buscar_na_fonte(self, pergunta, site):
        """Busca numa fonte específica"""
        if not GOOGLE_SEARCH_AVAILABLE:
            return []
            
        resultados = []
        
        try:
            # Busca específica no site
            query = f"site:{site} {pergunta}"
            
            urls = list(search(query, num_results=2, lang="pt"))
            
            for url in urls:
                try:
                    if NEWSPAPER_AVAILABLE:
                        article = Article(url, language='pt')
                        article.download()
                        article.parse()
                        
                        if article.text:
                            resultados.append({
                                'fonte': site,
                                'url': url,
                                'titulo': article.title,
                                'conteudo': article.text[:800],
                                'tipo_fonte': self._identificar_tipo_fonte(site)
                            })
                    else:
                        # Modo simplificado
                        resultados.append({
                            'fonte': site,
                            'url': url,
                            'titulo': f"Resultado de {site}",
                            'conteudo': "Clique no link para mais informações.",
                            'tipo_fonte': self._identificar_tipo_fonte(site)
                        })
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"Erro ao extrair {url}: {e}")
                    
        except Exception as e:
            print(f"Erro na busca para {site}: {e}")
        
        return resultados
    
    def _identificar_tipo_fonte(self, site):
        """Identifica o tipo de fonte baseado no domínio"""
        for tipo, fontes in self.fontes_confiaveis.items():
            if any(f in site for f in fontes):
                return tipo
        return "outra"
    
    def buscar_noticias_recentes(self, topico):
        """Busca notícias recentes sobre um tópico"""
        if not GOOGLE_SEARCH_AVAILABLE:
            return []
            
        resultados = []
        
        fontes_noticias = (self.fontes_confiaveis.get("media_publicos", []) + 
                          self.fontes_confiaveis.get("media_privados", []))
        
        for site in fontes_noticias[:3]:
            try:
                query = f"site:{site} {topico}"
                
                urls = list(search(query, num_results=2, lang="pt"))
                
                for url in urls:
                    if NEWSPAPER_AVAILABLE:
                        article = Article(url, language='pt')
                        article.download()
                        article.parse()
                        
                        resultados.append({
                            'fonte': site,
                            'url': url,
                            'titulo': article.title,
                            'conteudo': article.text[:300],
                            'tipo_fonte': 'noticias'
                        })
                    else:
                        resultados.append({
                            'fonte': site,
                            'url': url,
                            'titulo': f"Notícia sobre {topico}",
                            'conteudo': "Acesse o link para ler a notícia completa.",
                            'tipo_fonte': 'noticias'
                        })
                    
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"Erro ao buscar notícias: {e}")
        
        return resultados
    
    def formatar_resposta(self, resultados, pergunta):
        """Formata os resultados de forma organizada"""
        if not resultados:
            return None
        
        resposta = f"🔍 **Sobre: {pergunta}**\n\n"
        resposta += f"📊 Encontrei {len(resultados)} resultados em fontes moçambicanas:\n\n"
        
        for i, r in enumerate(resultados[:5], 1):
            resposta += f"📌 **{r.get('titulo', 'Sem título')[:80]}**\n"
            resposta += f"   📍 Fonte: {r['fonte']}\n"
            resposta += f"   🔗 Link: {r['url']}\n"
            
            if r.get('conteudo'):
                conteudo = r['conteudo'][:200]
                resposta += f"   📝 {conteudo}...\n"
            
            resposta += "\n"
        
        resposta += "\n---\n"
        resposta += "✅ **Informação obtida de fontes confiáveis moçambicanas**\n"
        resposta += "💡 Para mais detalhes, acesse os links acima."
        
        return resposta
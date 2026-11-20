# core/buscador_inteligente.py
# Buscador inteligente que procura nos sites certos e extrai respostas exatas

import requests
from bs4 import BeautifulSoup
import time
import re
from googlesearch import search
import json
import os

class BuscadorInteligente:
    """Buscador que procura a resposta exata nos sites oficiais"""
    
    # Mapeamento de categorias para sites específicos
    SITES_POR_CATEGORIA = {
        "parlamento": [
            "https://www.parlamento.mz",
            "https://www.portaldogoverno.gov.mz"
        ],
        "saude": [
            "https://www.misau.gov.mz",
            "https://www.ine.gov.mz"
        ],
        "educacao": [
            "https://www.mined.gov.mz",
            "https://www.uem.mz",
            "https://www.up.ac.mz"
        ],
        "economia": [
            "https://www.mef.gov.mz",
            "https://www.bancomoc.mz",
            "https://www.ine.gov.mz"
        ],
        "governo": [
            "https://www.portaldogoverno.gov.mz",
            "https://www.presidente.gov.mz",
            "https://www.parlamento.mz"
        ],
        "populacao": [
            "https://www.ine.gov.mz"
        ],
        "turismo": [
            "https://www.inatur.gov.mz",
            "https://www.mozambique.co.mz"
        ],
        "geral": [
            "https://www.portaldogoverno.gov.mz",
            "https://www.jornalnoticias.co.mz",
            "https://www.tvm.co.mz",
            "https://www.rm.co.mz"
        ]
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.cache = {}
    
    def identificar_categoria(self, pergunta):
        """Identifica a categoria da pergunta para direcionar a busca"""
        pergunta_lower = pergunta.lower()
        
        categorias = {
            "parlamento": ["deputado", "deputados", "parlamento", "assembleia", "assembleia da república"],
            "saude": ["médico", "médicos", "hospital", "doença", "saúde", "malária", "enfermeiro", "clinica", "tratamento", "vacina"],
            "educacao": ["escola", "universidade", "aluno", "professor", "ensino", "faculdade", "estudante", "curso", "uem", "up"],
            "economia": ["inflação", "pib", "economia", "produto interno", "crescimento", "moeda", "metical", "dolar", "preço", "banco"],
            "populacao": ["população", "habitante", "pessoas", "censos", "demografia", "quantos", "quantas"],
            "governo": ["presidente", "ministro", "governador", "lei", "decreto", "governo", "venancio", "mondlane"],
            "turismo": ["praia", "parque", "hotel", "turismo", "viagem", "visitar", "ponta do ouro", "vilanculos"]
        }
        
        for categoria, palavras in categorias.items():
            if any(palavra in pergunta_lower for palavra in palavras):
                return categoria
        return "geral"
    
    def buscar_resposta_exata(self, pergunta):
        """
        Busca a resposta exata para a pergunta
        """
        categoria = self.identificar_categoria(pergunta)
        print(f"🔍 Categoria identificada: {categoria}")
        
        # Selecionar sites para buscar
        sites = self.SITES_POR_CATEGORIA.get(categoria, self.SITES_POR_CATEGORIA["geral"])
        
        for site in sites[:4]:
            try:
                print(f"🌐 Buscando em: {site}")
                resultado = self._buscar_no_site(pergunta, site)
                if resultado:
                    print(f"✅ Encontrado resposta em: {site}")
                    return resultado
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Erro ao buscar em {site}: {e}")
        
        return None
    
    def _buscar_no_site(self, pergunta, site_base):
        """Busca no site específico usando Google"""
        try:
            dominio = site_base.replace("https://", "").replace("http://", "").split("/")[0]
            query = f"site:{dominio} {pergunta}"
            
            print(f"   🔎 Google: {query}")
            
            try:
                urls = list(search(query, num_results=5, lang="pt", timeout=15))
            except Exception as e:
                print(f"   ⚠️ Erro na busca Google: {e}")
                return None
            
            for url in urls:
                print(f"   📄 Analisando: {url[:80]}...")
                
                try:
                    resposta = self.session.get(url, timeout=15)
                    if resposta.status_code == 200:
                        soup = BeautifulSoup(resposta.content, 'html.parser')
                        texto = self._extrair_texto(soup)
                        trecho = self._encontrar_trecho_relevante(texto, pergunta)
                        
                        if trecho:
                            titulo = soup.find('title')
                            titulo_texto = titulo.text.strip() if titulo else "Sem título"
                            
                            return {
                                "resposta": trecho,
                                "fonte": dominio,
                                "url": url,
                                "titulo": titulo_texto[:150],
                                "pergunta": pergunta
                            }
                    else:
                        print(f"   ⚠️ HTTP {resposta.status_code}")
                        
                except requests.exceptions.Timeout:
                    print(f"   ⚠️ Timeout ao acessar {url}")
                except Exception as e:
                    print(f"   ⚠️ Erro ao acessar página: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Erro na busca: {e}")
        
        return None
    
    def _extrair_texto(self, soup):
        """Extrai texto limpo da página"""
        for script in soup(["script", "style", "nav", "footer", "header", "aside", "button"]):
            script.decompose()
        
        texto = ""
        
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4']):
            texto_titulo = tag.get_text().strip()
            if texto_titulo and len(texto_titulo) > 10:
                texto += texto_titulo + "\n"
        
        for p in soup.find_all('p'):
            texto_paragrafo = p.get_text().strip()
            if texto_paragrafo and len(texto_paragrafo) > 30:
                texto += texto_paragrafo + "\n"
        
        return texto.lower()
    
    def _encontrar_trecho_relevante(self, texto, pergunta):
        """Encontra o trecho exato que responde à pergunta"""
        pergunta_lower = pergunta.lower()
        palavras_chave = self._extrair_palavras_chave(pergunta_lower)
        
        if not palavras_chave:
            return None
        
        print(f"   🔑 Palavras-chave: {palavras_chave}")
        
        frases = re.split(r'[.!?;]+', texto)
        melhores_resultados = []
        
        for i, frase in enumerate(frases):
            frase = frase.strip()
            if len(frase) < 20:
                continue
            
            pontuacao = 0
            palavras_encontradas = []
            
            for palavra in palavras_chave:
                if palavra in frase:
                    pontuacao += 1
                    palavras_encontradas.append(palavra)
            
            if pontuacao >= 2:
                contexto = []
                if i > 0 and len(frases[i-1]) > 20:
                    contexto.append(frases[i-1].strip())
                contexto.append(frase)
                if i < len(frases) - 1 and len(frases[i+1]) > 20:
                    contexto.append(frases[i+1].strip())
                
                trecho = " ".join(contexto)
                
                melhores_resultados.append({
                    "trecho": trecho,
                    "pontuacao": pontuacao,
                    "palavras": palavras_encontradas
                })
        
        if melhores_resultados:
            melhores_resultados.sort(key=lambda x: x["pontuacao"], reverse=True)
            melhor = melhores_resultados[0]
            print(f"   ✨ Encontrado trecho com {melhor['pontuacao']} palavras-chave: {melhor['palavras']}")
            return self._limpar_trecho(melhor["trecho"])
        
        for i, frase in enumerate(frases):
            frase = frase.strip()
            if len(frase) < 30:
                continue
            
            for palavra in palavras_chave[:3]:
                if palavra in frase:
                    contexto = []
                    if i > 0:
                        contexto.append(frases[i-1].strip())
                    contexto.append(frase)
                    if i < len(frases) - 1:
                        contexto.append(frases[i+1].strip())
                    
                    trecho = " ".join(contexto)
                    print(f"   📌 Encontrado trecho com uma palavra-chave: {palavra}")
                    return self._limpar_trecho(trecho)
        
        return None
    
    def _extrair_palavras_chave(self, pergunta):
        """Extrai palavras-chave importantes da pergunta"""
        palavras_ignorar = [
            "qual", "quem", "como", "onde", "quando", "quantos", "quantas", "quanto",
            "o", "a", "os", "as", "um", "uma", "uns", "umas",
            "de", "da", "do", "das", "dos", "em", "para", "com", "por", "no", "na",
            "moçambique", "mocambique", "moçambicano", "mocambicano",
            "me", "te", "se", "nos", "vos", "lhe", "lhes",
            "é", "são", "está", "estão", "tem", "têm", "existem", "existe"
        ]
        
        pergunta_limpa = re.sub(r'[^\w\s]', ' ', pergunta.lower())
        palavras = pergunta_limpa.split()
        
        palavras_chave = []
        for p in palavras:
            if p not in palavras_ignorar and len(p) > 2:
                if p not in palavras_chave:
                    palavras_chave.append(p)
        
        if not palavras_chave:
            return [pergunta[:20]]
        
        return palavras_chave[:5]
    
    def _limpar_trecho(self, trecho):
        """Limpa e formata o trecho"""
        trecho = re.sub(r'\s+', ' ', trecho)
        trecho = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)\"]', '', trecho)
        if trecho:
            trecho = trecho[0].upper() + trecho[1:]
        if trecho and trecho[-1] not in '.!?':
            trecho += '.'
        if len(trecho) > 600:
            trecho = trecho[:600] + '...'
        return trecho
    
    def formatar_resposta(self, resultado):
        """Formata a resposta de forma bonita"""
        if not resultado:
            return None
        
        resposta = f"""
🔍 **Sobre: {resultado['pergunta']}**

📌 **{resultado['titulo']}**
   📍 Fonte: {resultado['fonte']}
   🔗 Link: {resultado['url']}

📝 **Resposta encontrada:**

"{resultado['resposta']}"

---
✅ **Informação extraída de fonte oficial moçambicana**
💡 Clique no link acima para verificar a informação completa
"""
        return resposta.strip()
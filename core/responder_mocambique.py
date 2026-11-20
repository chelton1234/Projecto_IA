# core/responder_mocambique.py
# Responder principal com Sociedade de Agentes IA e Filtro Geográfico
# Arquitetura: Filtro → Agente Local → Agente Busca → Agente Grounding

import random
import os
import json
from datetime import datetime
from core.gerenciador_conteudo import GerenciadorConteudo
from core.buscador_inteligente import BuscadorInteligente
from core.agentes.sociedade import SociedadeAgentes
from core.filtro_contexto import FiltroContexto

class ResponderMocambique:
    """Responder com Sociedade de Agentes IA e filtro apenas Moçambique"""
    
    def __init__(self):
        self.gerenciador = GerenciadorConteudo()
        self.buscador_inteligente = BuscadorInteligente()
        self.filtro = FiltroContexto()  # Filtro para apenas Moçambique
        
        # Carregar API key para grounding
        api_key = self._carregar_api_key()
        
        # Criar sociedade de agentes
        self.sociedade = SociedadeAgentes(
            self.gerenciador,
            self.buscador_inteligente,
            api_key
        )
        
        # Carregar configurações
        self.modo_busca = self._carregar_configuracao()
        self.ultimas_buscas = []
        
        # Respostas padrão (fallback)
        self.respostas_padrao = [
            "🌍 **Não encontrei essa informação específica sobre Moçambique.**\n\n"
            "📚 Tenta reformular a pergunta ou perguntar de outra forma.\n\n"
            "💡 Exemplos de perguntas que funcionam bem:\n"
            "• Quantos médicos tem Moçambique?\n"
            "• Qual é a taxa de inflação atual?\n"
            "• Quem é o governador de Nampula?\n"
            "• Qual é o salário mínimo em Moçambique?",
            
            "🇲🇿 **Não consegui encontrar uma resposta precisa.**\n\n"
            "🔍 Dicas para obter melhores resultados:\n"
            "• Usa palavras-chave como: dados, números, oficial\n"
            "• Sê específico(a) na pergunta\n"
            "• Inclui o nome da instituição se souberes",
            
            "📖 **Ainda estou a aprender, mas posso pesquisar!**\n\n"
            "🔎 Tenta perguntar sobre:\n"
            "• Dados estatísticos (população, médicos, escolas)\n"
            "• Informações governamentais (ministros, governadores)\n"
            "• Economia (inflação, moeda, PIB)\n"
            "• Saúde e educação\n"
            "• Turismo e cultura"
        ]
    
    def _carregar_api_key(self):
        """Carrega API key do config"""
        try:
            if os.path.exists("config/api_config.json"):
                with open("config/api_config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get("gemini", {}).get("api_key")
        except Exception as e:
            print(f"Erro ao carregar API key: {e}")
        return None
    
    def _carregar_configuracao(self):
        """Carrega configuração do modo de busca"""
        try:
            if os.path.exists("config/config.json"):
                with open("config/config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    modo = config.get("modo_padrao", "hibrido")
                    return modo if modo in ("local", "web", "hibrido") else "hibrido"
        except:
            pass
        return "hibrido"
    
    def gerar_resposta(self, pergunta):
        """Gera resposta - APENAS sobre Moçambique"""
        if not pergunta.strip():
            return "🇲🇿 Por favor, digite uma pergunta sobre Moçambique."
        
        # 🔒 FILTRO GEOGRÁFICO - Verificar se é sobre Moçambique
        aceite, mensagem_erro = self.filtro.validar(pergunta)
        
        if not aceite:
            print(f"🚫 Pergunta bloqueada: {pergunta[:50]}...")
            return mensagem_erro
        
        print(f"\n{'='*60}")
        print(f"📝 Processando pergunta sobre Moçambique: {pergunta}")
        print(f"{'='*60}")
        
        # Usar sociedade de agentes com o modo actual
        resposta = self.sociedade.processar_pergunta(pergunta, self.modo_busca)
        
        if resposta:
            return resposta
        
        # Fallback para respostas padrão
        print("⚠️ Nenhuma resposta encontrada pela sociedade")
        self.registrar_pergunta_nao_respondida(pergunta)
        return random.choice(self.respostas_padrao)
    
    def registrar_pergunta_nao_respondida(self, pergunta):
        """Regista perguntas para melhorias futuras"""
        try:
            with open("dados/perguntas_nao_respondidas_mz.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {pergunta}\n")
        except Exception as e:
            print(f"Erro ao registar pergunta: {e}")
    
    def alternar_modo_busca(self, modo=None):
        """Alterna entre modos de busca"""
        modos = ["hibrido", "web", "local"]

        if modo in modos:
            self.modo_busca = modo
        elif self.modo_busca in modos:
            idx = modos.index(self.modo_busca)
            self.modo_busca = modos[(idx + 1) % len(modos)]
        else:
            self.modo_busca = "hibrido"

        descricoes = {
            "local": "Apenas base local (mais rápido, conteúdo limitado)",
            "web": "Google Search + base local como fallback",
            "hibrido": "Sociedade de Agentes (recomendado)"
        }
        
        return f"🌐 Modo de busca alterado para: **{self.modo_busca.upper()}**\n{descricoes[self.modo_busca]}"
    
    def obter_estatisticas(self):
        """Retorna estatísticas detalhadas"""
        # Calcular total de tópicos locais
        topicos_locais = 0
        if hasattr(self.gerenciador, 'base_conhecimento'):
            if isinstance(self.gerenciador.base_conhecimento, dict):
                topicos_locais = len(self.gerenciador.base_conhecimento)
            else:
                topicos_locais = 1
        
        # Contar fontes configuradas no buscador inteligente
        fontes_configuradas = 0
        try:
            for categoria in self.buscador_inteligente.SITES_POR_CATEGORIA:
                fontes_configuradas += len(self.buscador_inteligente.SITES_POR_CATEGORIA[categoria])
        except:
            fontes_configuradas = 35
        
        # Obter estatísticas do filtro
        stats_filtro = self.filtro.get_estatisticas()

        grounding = next((a for a in self.sociedade.agentes if a.tipo == "web"), None)
        if grounding and getattr(grounding, "disponivel", False):
            ia_status = "Ativa (Gemini + Google Search)"
        else:
            ia_status = "Indisponível (modo local)"

        return {
            "modo_busca": self.modo_busca,
            "topicos_locais": topicos_locais,
            "buscas_realizadas": len(self.ultimas_buscas),
            "fontes_configuradas": fontes_configuradas,
            "categorias": len(self.buscador_inteligente.SITES_POR_CATEGORIA),
            "ia_status": ia_status,
            "filtro": stats_filtro
        }
    
    def mostrar_ajuda(self):
        """Mostra ajuda com a sociedade de agentes"""
        status_sociedade = self.sociedade.get_status()
        stats_filtro = self.filtro.get_estatisticas()
        
        ajuda = f"""
        🤖 **MozAssist Pro - Sociedade de Agentes IA**
        
        {status_sociedade}
        
        📊 **Filtro de Moçambique:**
        • Perguntas aceites: {stats_filtro['aceites']}
        • Perguntas bloqueadas: {stats_filtro['bloqueadas']}
        • Taxa de aceitação: {stats_filtro['taxa_aceitacao']}%
        
        📝 **Como funciona:**
        
        Cada pergunta é processada por agentes especializados em ordem:
        
        1️⃣ **Agente Local** - Respostas instantâneas (capital, presidente, moeda)
        2️⃣ **Agente Busca** - Busca em sites oficiais (.gov.mz, INE, Banco de Moçambique)
        3️⃣ **Agente Grounding** - Pesquisa Google + IA (para informações atualizadas)
        
        🔍 **Exemplos de perguntas:**
        
        • **Agente Local:** "Qual é a capital?" "Quem é o presidente?"
        • **Agente Busca:** "Quantos médicos tem Moçambique?" "Taxa de inflação?"
        • **Agente Grounding:** "Últimas notícias" "Cotação do metical hoje"
        
        🔧 **Comandos especiais:**
        • "alternar modo" - Troca entre local/híbrido
        • "estatísticas" - Mostra dados do sistema
        • "ajuda" - Mostra esta mensagem
        
        🌐 **Fontes oficiais consultadas:**
        • Portais do Governo (.gov.mz)
        • Banco de Moçambique
        • Instituto Nacional de Estatística (INE)
        • Ministério da Saúde (MISAU)
        • Televisão de Moçambique (TVM)
        
        💡 **Dica:** Quanto mais específica for a pergunta, melhor será a resposta!
        """
        return ajuda
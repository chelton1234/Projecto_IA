# core/integrador_ia.py
# Integração com a nova API Google GenAI (Gemini)

import os
import json

class IntegradorIA:
    """Integra o chatbot com a nova API Google GenAI (Gemini)"""
    
    def __init__(self):
        self.config = self.carregar_config()
        self.api_key = self.config.get("gemini", {}).get("api_key", "")
        self.modelo_nome = self.config.get("gemini", {}).get("modelo", "gemini-2.0-flash")
        self.modelo_completo = f"models/{self.modelo_nome}"
        self.disponivel = self.verificar_disponibilidade()
        
        if self.disponivel:
            print(f"✅ API Gemini (GenAI) configurada - Modelo: {self.modelo_completo}")
        else:
            print("⚠️ API Gemini não configurada. Modo IA desativado.")
    
    def carregar_config(self):
        """Carrega configuração da API"""
        try:
            if os.path.exists("config/api_config.json"):
                with open("config/api_config.json", 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
        return {"gemini": {"api_key": ""}, "usar_ia_quando_nao_encontrar": False}
    
    def verificar_disponibilidade(self):
        """Verifica se a API está configurada"""
        if not self.api_key:
            return False
        return True
    
    def gerar_resposta(self, pergunta, contexto=""):
        """Gera resposta usando a nova API Google GenAI (Gemini)"""
        
        if not self.disponivel:
            return None
        
        try:
            from google import genai
            
            # Configurar o cliente
            client = genai.Client(api_key=self.api_key)
            
            # Criar o prompt
            prompt = f"""
            Você é um assistente especialista em Moçambique.
            
            REGRAS IMPORTANTES:
            1. Use apenas informações precisas e factuais sobre Moçambique
            2. Se não souber a resposta, diga que não tem informação
            3. Não invente dados ou informações
            4. Seja objetivo, direto e conciso
            5. Responda em português de Moçambique
            
            Pergunta do usuário: {pergunta}
            
            Resposta:
            """
            
            # Gerar resposta
            response = client.models.generate_content(
                model=self.modelo_completo,
                contents=prompt
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                return None
                
        except ImportError:
            print("⚠️ Biblioteca google-genai não instalada")
            print("   Instale com: pip install google-genai")
            return None
        except Exception as e:
            print(f"❌ Erro na API Gemini: {e}")
            return None
    
    def formatar_resposta_ia(self, resposta, pergunta):
        """Formata a resposta da IA para exibição"""
        if not resposta:
            return None
        
        return f"""
🤖 **Resposta gerada por IA (Google Gemini)**

🔍 **Sobre:** {pergunta}

📝 **Resposta:**
{resposta}

---
⚠️ **Nota:** Esta resposta foi gerada por Inteligência Artificial.
Recomenda-se verificar as informações em fontes oficiais moçambicanas.
"""
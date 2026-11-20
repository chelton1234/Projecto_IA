#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MozAssist Pro - Chatbot Especializado em Moçambique
Versão: 3.0 com 3 camadas: Base Local → Busca Oficial → IA (Gemini)
"""

import sys
import os
import json
from datetime import datetime

# Adicionar diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.responder_mocambique import ResponderMocambique
from interface_avancada import InterfaceAvancada

def verificar_estrutura():
    """Verifica se toda a estrutura de pastas existe"""
    
    pastas = [
        "dados",
        "dados/documentos",
        "config",
        "testes",
        "logs",
        "utils"
    ]
    
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📁 Pasta criada: {pasta}")

def mostrar_banner():
    """Mostra banner de inicialização"""
    
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🇲🇿  MOZASSIST PRO - Chatbot Especializado               ║
    ║      Informações Confiáveis sobre Moçambique                ║
    ║                                                              ║
    ║   Versão: 3.0                                               ║
    ║   Camadas: Base Local → Sites Oficiais → IA (Gemini)        ║
    ║   Fontes: Governo, TVs, Jornais, INE, Banco de Moçambique   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    print(banner)

def main():
    """Função principal do programa"""
    
    mostrar_banner()
    
    print("\n🔧 Verificando estrutura do projeto...")
    verificar_estrutura()
    
    print("\n🚀 Inicializando componentes...")
    
    try:
        # Inicializar responder
        responder = ResponderMocambique()
        
        # Obter estatísticas
        stats = responder.obter_estatisticas()
        
        print(f"\n📊 Estatísticas do Sistema:")
        print(f"   • Modo de busca: {stats['modo_busca'].upper()}")
        print(f"   • Tópicos locais: {stats['topicos_locais']}")
        print(f"   • Fontes configuradas: {stats['fontes_configuradas']}")
        print(f"   • Buscas realizadas: {stats['buscas_realizadas']}")
        print(f"   • Status IA: {stats.get('ia_status', 'Desativada')}")
        
        # Mensagem sobre a IA
        if stats.get('ia_status', '').startswith('Ativa'):
            print(f"\n🤖 IA ATIVA: Google Gemini pronto para responder!")
        else:
            print(f"\n⚠️ IA DESATIVADA: Configure a API key em config/api_config.json")
            print(f"   Obtenha uma chave gratuita em: https://makersuite.google.com/app/apikey")
        
        print("\n🖥️  Abrindo interface gráfica...")
        print("   (A janela do chatbot vai abrir em instantes)\n")
        
        # Iniciar interface
        app = InterfaceAvancada(responder)
        app.iniciar()
        
    except Exception as e:
        print(f"\n❌ Erro ao iniciar o chatbot: {e}")
        
        # Registar erro
        try:
            with open("logs/erros.log", "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {str(e)}\n")
        except:
            pass
        
        input("\nPressione ENTER para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main()
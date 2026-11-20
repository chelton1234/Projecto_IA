# testes/test_responder.py
# Testes para o responder

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.responder_mocambique import ResponderMocambique
from core.filtro_contexto import FiltroContexto

def test_responder():
    """Testa o responder"""
    responder = ResponderMocambique()

    # Testar pergunta sobre capital
    resposta = responder.gerar_resposta("Qual é a capital de Moçambique?")
    assert "Maputo" in resposta, "Erro: resposta sobre capital incorreta"
    print("✅ Teste de pergunta sobre capital passou!")

    # Testar pergunta sobre províncias
    resposta = responder.gerar_resposta("Quais são as províncias?")
    assert "províncias" in resposta.lower() or "Maputo" in resposta, "Erro: resposta sobre províncias incorreta"
    print("✅ Teste de pergunta sobre províncias passou!")

    # Testar modos de busca
    for modo in ("web", "local", "hibrido"):
        responder.alternar_modo_busca(modo)
        assert responder.modo_busca == modo, f"Erro: modo {modo} não ativado"
    print("✅ Teste de alternar modo passou!")

    # Testar que perguntas genéricas são aceites
    filtro = FiltroContexto()
    aceite, _ = filtro.validar("Qual é a taxa de inflação atual?")
    assert aceite, "Erro: pergunta genérica foi bloqueada"
    print("✅ Teste do filtro de contexto passou!")

    print("✅ Todos os testes passaram!")

if __name__ == "__main__":
    test_responder()

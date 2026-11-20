import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.buscador_inteligente import BuscadorInteligente
from core.classificador_ml import ClassificadorIntencao
from core.gerenciador_conteudo import GerenciadorConteudo


def test_classificador():
    classificador = ClassificadorIntencao()
    casos = {
        "Quantos médicos tem Moçambique?": "saude",
        "Quais são as praias de Moçambique?": "turismo",
        "Qual é a taxa de inflação?": "economia",
        "Quem é o presidente do parlamento?": "parlamento",
    }
    for pergunta, esperado in casos.items():
        previsao = classificador.predizer(pergunta)
        assert previsao is not None, f"Sem previsão para: {pergunta}"
        assert previsao["categoria"] == esperado, f"{pergunta} -> {previsao}"

    metricas = classificador.obter_metricas()
    assert metricas.get("acuracia", 0) > 0.60, "Acurácia abaixo do esperado"
    assert metricas.get("f1_macro", 0) > 0.60, "F1-macro abaixo do esperado"
    print("✅ Classificador ML passou!")


def test_recuperacao_semantica():
    gerenciador = GerenciadorConteudo()
    resposta = gerenciador.buscar_por_similaridade("Como é o clima do país?")
    assert resposta is not None, "Não encontrou trecho por similaridade"
    print("✅ Recuperação por similaridade passou!")


def test_integracao():
    buscador = BuscadorInteligente()
    categoria = buscador.identificar_categoria("Quantos médicos tem Moçambique?")
    assert categoria == "saude", f"Categoria incorrecta: {categoria}"
    print("✅ Integração do ML no buscador passou!")


if __name__ == "__main__":
    test_classificador()
    test_recuperacao_semantica()
    test_integracao()
    print("✅ Todos os testes de ML passaram!")

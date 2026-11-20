import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.classificador_ml import ClassificadorIntencao


def main():
    classificador = ClassificadorIntencao()
    metricas = classificador.treinar(avaliar=True)

    print("=" * 60)
    print("Treinamento do classificador de intencao - MozAssist Pro")
    print("=" * 60)
    print(f"Exemplos: {metricas['total_exemplos']}")
    print(f"Acuracia: {metricas['acuracia']:.2%}")
    print(f"F1-macro: {metricas['f1_macro']:.2%}")
    print("\nRelatorio por categoria:")
    print(metricas["relatorio_texto"])
    print(f"Modelo guardado em: {classificador.caminho_modelo}")

    with open("dados/metricas_ml.json", "w", encoding="utf-8") as arquivo:
        json.dump(metricas, arquivo, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

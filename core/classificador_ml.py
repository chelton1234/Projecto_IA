import json
import os

import joblib
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from unidecode import unidecode


class ClassificadorIntencao:
    CAMINHO_DADOS = "dados/intencoes.json"
    CAMINHO_MODELO = "dados/modelos/intencao.joblib"

    def __init__(self, caminho_dados=None, caminho_modelo=None):
        self.caminho_dados = caminho_dados or self.CAMINHO_DADOS
        self.caminho_modelo = caminho_modelo or self.CAMINHO_MODELO
        self.modelo = None
        self.metricas = {}

    def normalizar(self, texto):
        return unidecode(str(texto)).lower()

    def carregar_dados(self):
        with open(self.caminho_dados, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        perguntas = [self.normalizar(item["pergunta"]) for item in dados]
        categorias = [item["categoria"] for item in dados]
        return perguntas, categorias

    def construir_modelo(self):
        return Pipeline([
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True)),
            ("classificador", CalibratedClassifierCV(LinearSVC(C=10), cv=3, method="sigmoid"))
        ])

    def treinar(self, avaliar=True):
        perguntas, categorias = self.carregar_dados()
        modelo = self.construir_modelo()

        if avaliar:
            preg_treino, preg_teste, cat_treino, cat_teste = train_test_split(
                perguntas, categorias, test_size=0.25, random_state=42, stratify=categorias
            )
            modelo.fit(preg_treino, cat_treino)
            previsoes = modelo.predict(preg_teste)
            self.metricas = {
                "acuracia": round(accuracy_score(cat_teste, previsoes), 4),
                "f1_macro": round(f1_score(cat_teste, previsoes, average="macro"), 4),
                "relatorio": classification_report(cat_teste, previsoes, output_dict=True, zero_division=0),
                "relatorio_texto": classification_report(cat_teste, previsoes, zero_division=0),
                "total_exemplos": len(perguntas),
                "categorias": sorted(set(categorias))
            }

        modelo.fit(perguntas, categorias)
        self.modelo = modelo
        self.salvar()
        return self.metricas

    def salvar(self):
        os.makedirs(os.path.dirname(self.caminho_modelo), exist_ok=True)
        joblib.dump({"modelo": self.modelo, "metricas": self.metricas}, self.caminho_modelo)

    def carregar(self):
        if not os.path.exists(self.caminho_modelo):
            return False
        try:
            dados = joblib.load(self.caminho_modelo)
            self.modelo = dados["modelo"]
            self.metricas = dados.get("metricas", {})
            return True
        except Exception:
            return False

    def garantir_modelo(self):
        if self.modelo is None and not self.carregar():
            self.treinar(avaliar=False)

    def predizer(self, pergunta, limiar=0.30):
        self.garantir_modelo()
        if self.modelo is None:
            return None

        probabilidades = self.modelo.predict_proba([self.normalizar(pergunta)])[0]
        indice = probabilidades.argmax()
        confianca = float(probabilidades[indice])
        if confianca < limiar:
            return None

        return {
            "categoria": str(self.modelo.classes_[indice]),
            "confianca": round(confianca, 3)
        }

    def obter_metricas(self):
        self.garantir_modelo()
        return self.metricas

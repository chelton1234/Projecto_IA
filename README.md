# MozAssist Pro - Chatbot Especializado em Moçambique 🇲🇿

## Sobre o Projeto
Chatbot inteligente que fornece informações precisas e confiáveis sobre Moçambique, utilizando fontes oficiais, pesquisa em tempo real e IA (Google Gemini).

## Funcionalidades
- **Machine Learning**: classificador de intenção (TF-IDF + SVM calibrado) treinado com 312 perguntas rotuladas em 8 categorias
- Recuperação por similaridade semântica (TF-IDF + cosine) sobre a base de conhecimento local
- Respostas em tempo real via Google Search + Gemini
- Busca em sites oficiais (.gov.mz, INE, Banco de Moçambique)
- Base local com fatos imutáveis (capital, províncias, moeda, etc.)
- Modos: `hibrido` (recomendado), `web` e `local`
- Interface web (Flask) e interface gráfica (Tkinter)

## Instalação
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config/api_config.example.json config/api_config.json
```

Edite `config/api_config.json` e coloque a sua chave da API do Gemini.
O ficheiro `config/api_config.json` está ignorado pelo Git e nunca deve ser publicado.

## Como executar
Versão web (recomendada):
```bash
python3 app.py
```
Acesse em http://localhost:5000

Versão gráfica:
```bash
python3 main.py
```

## Machine Learning
O classificador prevê a categoria da pergunta e direcciona a busca para as fontes oficiais adequadas.

```bash
python3 treinar_modelo.py
```

Resultados da validação (25% dos dados, estratificado):

| Métrica | Valor |
| --- | --- |
| Acurácia | 78,21% |
| F1-macro | 77,51% |
| Exemplos rotulados | 312 |
| Categorias | 8 |

O modelo é guardado em `dados/modelos/` (ignorado pelo Git) e é treinado automaticamente na primeira execução se não existir.

## Testes
```bash
python3 testes/test_responder.py
python3 testes/test_ml.py
```

## Fontes Utilizadas
- 🏛️ **Governamentais**: Portais oficiais do governo
- 📺 **Media Públicos**: TVM, RM, Jornal Notícias
- 📰 **Media Privados**: O País, Canal Moz, Verdade
- 🎓 **Instituições**: INE, Banco de Moçambique, UEM
- 🌴 **Turismo**: INATUR, Visit Mozambique

## Estrutura do Projeto
```
app.py              Servidor web Flask
main.py             Interface gráfica Tkinter
core/               Agentes, buscadores e filtro de contexto
config/             Configurações (a API key não é versionada)
dados/              Base de conhecimento, dataset rotulado e métricas ML
static/, templates/ Interface web
testes/             Testes automatizados
```

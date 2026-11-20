# MozAssist Pro - Chatbot Especializado em Moçambique 🇲🇿

## Sobre o Projeto
Chatbot inteligente que fornece informações precisas e confiáveis sobre Moçambique, utilizando fontes oficiais, pesquisa em tempo real e IA (Google Gemini).

## Funcionalidades
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

## Testes
```bash
python3 testes/test_responder.py
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
dados/              Base de conhecimento local
static/, templates/ Interface web
testes/             Testes automatizados
```

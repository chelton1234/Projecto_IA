# app.py
# Aplicação web do MozAssist Pro

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Adicionar diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.responder_mocambique import ResponderMocambique

app = Flask(__name__)
CORS(app)

# Inicializar o chatbot
responder = ResponderMocambique()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint da API para enviar mensagens"""
    try:
        data = request.get_json()
        pergunta = data.get('pergunta', '')
        
        if not pergunta:
            return jsonify({'erro': 'Pergunta vazia'}), 400
        
        # Gerar resposta
        resposta = responder.gerar_resposta(pergunta)
        
        # Obter estatísticas
        stats = responder.obter_estatisticas()
        
        return jsonify({
            'resposta': resposta,
            'status': 'success',
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'erro': str(e),
            'status': 'error'
        }), 500

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    """Endpoint para obter estatísticas"""
    try:
        stats = responder.obter_estatisticas()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/alternar_modo', methods=['POST'])
def alternar_modo():
    """Endpoint para alternar modo de busca"""
    try:
        data = request.get_json()
        modo = data.get('modo', None)
        msg = responder.alternar_modo_busca(modo)
        return jsonify({'mensagem': msg, 'modo': responder.modo_busca})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🌐 MozAssist Pro - Versão Web")
    print("="*60)
    print("\n🚀 Servidor iniciado!")
    print("📱 Acesse no navegador: http://localhost:5000")
    print("🔴 Para parar: Ctrl+C")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
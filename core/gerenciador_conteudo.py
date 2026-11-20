# core/gerenciador_conteudo.py
# Gerencia a base de conhecimento local sobre Moçambique

import json
import os
from datetime import datetime

class GerenciadorConteudo:
    """Gerencia a base de conhecimento local com informações de Moçambique"""
    
    def __init__(self):
        self.caminho_base = "dados/conhecimento_mocambique.json"
        self.base_conhecimento = self.carregar_base()
        
    def carregar_base(self):
        """Carrega a base de conhecimento de Moçambique"""
        if os.path.exists(self.caminho_base):
            try:
                with open(self.caminho_base, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.criar_base_padrao()
        else:
            return self.criar_base_padrao()
    
    def criar_base_padrao(self):
        """Cria base de conhecimento inicial sobre Moçambique"""
        base = {
            "sobre_mocambique": {
                "nome_oficial": "República de Moçambique",
                "capital": "Maputo",
                "lingua_oficial": "Português",
                "moeda": "Metical (MZN)",
                "populacao": "± 33 milhões (2024)",
                "area": "801.590 km²",
                "presidente": "Daniel Chapo (2025-presente)",
                "independencia": "25 de junho de 1975",
                "gentilico": "Moçambicano(a)",
                "fuso_horario": "UTC+2"
            },
            "provincias": [
                {"nome": "Maputo Cidade", "capital": "Maputo", "area": "300 km²"},
                {"nome": "Maputo Província", "capital": "Matola", "area": "22.693 km²"},
                {"nome": "Gaza", "capital": "Xai-Xai", "area": "75.709 km²"},
                {"nome": "Inhambane", "capital": "Inhambane", "area": "68.615 km²"},
                {"nome": "Manica", "capital": "Chimoio", "area": "61.661 km²"},
                {"nome": "Sofala", "capital": "Beira", "area": "68.018 km²"},
                {"nome": "Tete", "capital": "Tete", "area": "100.724 km²"},
                {"nome": "Zambézia", "capital": "Quelimane", "area": "105.008 km²"},
                {"nome": "Nampula", "capital": "Nampula", "area": "81.606 km²"},
                {"nome": "Niassa", "capital": "Lichinga", "area": "129.055 km²"},
                {"nome": "Cabo Delgado", "capital": "Pemba", "area": "82.625 km²"}
            ],
            "cultura": {
                "grupos_etnicos": ["Makhuwa", "Tsonga", "Lomwe", "Sena", "Shona", "Ndau", "Chopi", "Swahili"],
                "musica_tradicional": ["Marrabenta", "Pandza", "Timbila", "Chigubo"],
                "instrumentos": ["Timbila", "Mbira", "Djembe", "Xipendana"],
                "gastronomia": ["Matapa", "Xima", "Peixe grelhado", "Piri-piri", "Camarao", "Caril de amendoim"],
                "bebidas_tipicas": ["Cajú", "Tipo Tinto", "Laurentina", "2M"],
                "arte": ["Escultura em madeira", "Mucapata", "Capulana", "Cestaria"],
                "festas_tradicionais": ["Nyau", "Tufo", "Lobolo", "Cerimónia do Chicualacuala"]
            },
            "economia": {
                "principais_setores": ["Agricultura", "Mineração", "Turismo", "Energia", "Indústria"],
                "principais_produtos": ["Cajú", "Algodão", "Açúcar", "Gás natural", "Carvão", "Titânio", "Madeira"],
                "pib_2024": "± 20 mil milhões USD",
                "principais_parceiros": ["África do Sul", "China", "Índia", "Portugal", "EUA"],
                "recursos_naturais": ["Gás natural", "Carvão", "Grafite", "Rubis", "Madeira", "Energia hidroelétrica"]
            },
            "turismo": {
                "praias": ["Ponta do Ouro", "Tofo", "Vilanculos", "Bazaruto", "Quirimbas", "Pemba", "Inhaca"],
                "parques_nacionais": ["Gorongosa", "Maputo", "Bazaruto", "Quirimbas", "Limpopo", "Zinave", "Banhine"],
                "patrimonio_histórico": ["Ilha de Moçambique", "Fortaleza de Maputo", "Catedral da Beira", "Estaçao CFM"],
                "cidades_historicas": ["Ilha de Moçambique", "Maputo", "Inhambane", "Quelimane"]
            },
            "geografia": {
                "rios_principais": ["Zambeze", "Limpopo", "Save", "Rovuma", "Lúrio"],
                "lagos": ["Lago Niassa", "Lago Chiuta", "Lago Amaramba"],
                "montanhas": ["Monte Binga", "Monte Namuli", "Serra da Gorongosa"],
                "clima": "Tropical com duas estações: chuvosa (out-nov) e seca (abr-set)"
            },
            "saude": {
                "expectativa_vida": "± 60 anos",
                "principais_doencas": ["Malária", "HIV/SIDA", "Tuberculose"],
                "hospitais_referencia": ["Hospital Central de Maputo", "Hospital da Beira", "Hospital Central de Nampula"]
            },
            "educacao": {
                "taxa_alfabetizacao": "± 60%",
                "universidades": ["UEM", "UP", "ISCTEM", "UniLurio", "UniZambeze", "UniSave"],
                "anos_obrigatorios": "7 anos (ensino primário)"
            }
        }
        
        self.salvar_base(base)
        return base
    
    def salvar_base(self, base=None):
        """Salva a base de conhecimento"""
        if base:
            self.base_conhecimento = base
        
        with open(self.caminho_base, 'w', encoding='utf-8') as f:
            json.dump(self.base_conhecimento, f, ensure_ascii=False, indent=2)
    
    def buscar_local(self, pergunta):
        """Busca na base de conhecimento local"""
        pergunta_lower = pergunta.lower()
        
        # Capital
        if "capital" in pergunta_lower:
            return f"A capital de Moçambique é {self.base_conhecimento['sobre_mocambique']['capital']}."
        
        # Províncias
        if "província" in pergunta_lower or "provincia" in pergunta_lower:
            provincias = [p['nome'] for p in self.base_conhecimento['provincias']]
            return f"As 11 províncias de Moçambique são: {', '.join(provincias)}."
        
        # População
        if "população" in pergunta_lower or "populacao" in pergunta_lower:
            return f"Moçambique tem uma população estimada de {self.base_conhecimento['sobre_mocambique']['populacao']}."
        
        # Presidente
        if "presidente" in pergunta_lower:
            return f"O Presidente de Moçambique é {self.base_conhecimento['sobre_mocambique']['presidente']}."
        
        # Moeda
        if "moeda" in pergunta_lower:
            return f"A moeda oficial de Moçambique é o {self.base_conhecimento['sobre_mocambique']['moeda']}."
        
        # Língua
        if "língua" in pergunta_lower or "lingua" in pergunta_lower or "idioma" in pergunta_lower:
            return f"A língua oficial de Moçambique é o {self.base_conhecimento['sobre_mocambique']['lingua_oficial']}. Existem também várias línguas nacionais como {', '.join(self.base_conhecimento['cultura']['grupos_etnicos'][:3])}."
        
        # Praias
        if "praia" in pergunta_lower:
            praias = self.base_conhecimento['turismo']['praias']
            return f"As praias mais famosas de Moçambique são: {', '.join(praias[:8])}."
        
        # Parques
        if "parque" in pergunta_lower or "reserva" in pergunta_lower:
            parques = self.base_conhecimento['turismo']['parques_nacionais']
            return f"Os principais parques nacionais são: {', '.join(parques)}."
        
        # Gastronomia
        if "comida" in pergunta_lower or "gastronomia" in pergunta_lower or "prato" in pergunta_lower:
            comidas = self.base_conhecimento['cultura']['gastronomia']
            return f"A gastronomia moçambicana inclui: {', '.join(comidas)}."
        
        # Cultura
        if "cultura" in pergunta_lower:
            grupos = self.base_conhecimento['cultura']['grupos_etnicos']
            musica = self.base_conhecimento['cultura']['musica_tradicional']
            return f"Moçambique tem uma cultura rica com grupos étnicos como {', '.join(grupos[:5])}. Música tradicional inclui {', '.join(musica)}."
        
        # Economia
        if "economia" in pergunta_lower:
            setores = self.base_conhecimento['economia']['principais_setores']
            produtos = self.base_conhecimento['economia']['principais_produtos']
            return f"Os principais setores económicos são: {', '.join(setores)}. Principais produtos: {', '.join(produtos[:5])}."
        
        # Rios
        if "rio" in pergunta_lower:
            rios = self.base_conhecimento['geografia']['rios_principais']
            return f"Os principais rios de Moçambique são: {', '.join(rios)}."
        
        # Clima
        if "clima" in pergunta_lower or "temperatura" in pergunta_lower:
            return self.base_conhecimento['geografia']['clima']
        
        # Universidades
        if "universidade" in pergunta_lower or "faculdade" in pergunta_lower:
            universidades = self.base_conhecimento['educacao']['universidades']
            return f"As principais universidades são: {', '.join(universidades)}."
        
        return None
    
    def obter_todos_topicos(self):
        """Retorna lista de todos os tópicos disponíveis"""
        return list(self.base_conhecimento.keys())
    
    def obter_informacao_completa(self):
        """Retorna toda a informação para estatísticas"""
        return self.base_conhecimento
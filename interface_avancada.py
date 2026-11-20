# interface_avancada.py
# Interface gráfica profissional estilo web para MozAssist Pro

import tkinter as tk
from tkinter import scrolledtext, messagebox, font
import threading
import sys
import os
from datetime import datetime

class InterfaceAvancada:
    """Interface profissional estilo web para o chatbot"""
    
    def __init__(self, responder):
        self.responder = responder
        
        # Criar janela principal
        self.janela = tk.Tk()
        self.janela.title("MozAssist Pro - Informações Confiáveis sobre Moçambique")
        self.janela.geometry("1100x700")
        self.janela.minsize(900, 600)
        self.janela.configure(bg="#f8f9fc")
        
        # Cores profissionais
        self.cores = {
            "bg_principal": "#f8f9fc",
            "bg_lateral": "#1e2a3e",
            "bg_chat": "#ffffff",
            "primaria": "#2c7a2c",
            "primaria_escuro": "#1e5a1e",
            "primaria_claro": "#4a9e4a",
            "secundaria": "#ff6b35",
            "usuario_msg": "#e3f2fd",
            "bot_msg": "#f0f4f8",
            "texto_usuario": "#1e466e",
            "texto_bot": "#1e2a3e",
            "cinza_claro": "#e9ecef",
            "cinza_medio": "#adb5bd",
            "cinza_escuro": "#495057",
            "branco": "#ffffff",
            "sucesso": "#28a745",
            "info": "#17a2b8"
        }
        
        self.configurar_interface()
    
    def configurar_interface(self):
        """Configura toda a interface"""
        
        # Frame principal
        self.frame_principal = tk.Frame(self.janela, bg=self.cores["bg_principal"])
        self.frame_principal.pack(fill="both", expand=True)
        
        # ==================== BARRA LATERAL ====================
        self.criar_barra_lateral()
        
        # ==================== ÁREA PRINCIPAL ====================
        self.criar_area_principal()
        
        # Mensagem de boas-vindas
        self.mostrar_boas_vindas()
        
        # Focar na entrada
        self.entrada.focus()
    
    def criar_barra_lateral(self):
        """Cria barra lateral moderna"""
        
        self.frame_lateral = tk.Frame(
            self.frame_principal,
            bg=self.cores["bg_lateral"],
            width=280
        )
        self.frame_lateral.pack(side="left", fill="y")
        self.frame_lateral.pack_propagate(False)
        
        # Logo e título
        frame_logo = tk.Frame(self.frame_lateral, bg=self.cores["bg_lateral"], height=100)
        frame_logo.pack(fill="x", pady=(30, 20))
        frame_logo.pack_propagate(False)
        
        lbl_icon = tk.Label(
            frame_logo,
            text="🇲🇿",
            font=("Segoe UI Emoji", 40),
            bg=self.cores["bg_lateral"],
            fg=self.cores["primaria_claro"]
        )
        lbl_icon.pack()
        
        lbl_titulo = tk.Label(
            frame_logo,
            text="MozAssist Pro",
            font=("Segoe UI", 18, "bold"),
            bg=self.cores["bg_lateral"],
            fg=self.cores["branco"]
        )
        lbl_titulo.pack()
        
        lbl_sub = tk.Label(
            frame_logo,
            text="Informações de Moçambique",
            font=("Segoe UI", 9),
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_medio"]
        )
        lbl_sub.pack()
        
        # Separador
        self._criar_separador_lateral()
        
        # Status do sistema
        frame_status = tk.Frame(self.frame_lateral, bg=self.cores["bg_lateral"])
        frame_status.pack(fill="x", padx=20, pady=10)
        
        lbl_modo = tk.Label(
            frame_status,
            text="🔍 Modo de Busca",
            font=("Segoe UI", 10, "bold"),
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_claro"]
        )
        lbl_modo.pack(anchor="w")
        
        self.lbl_modo_valor = tk.Label(
            frame_status,
            text=self.responder.modo_busca.upper(),
            font=("Segoe UI", 10),
            bg=self.cores["bg_lateral"],
            fg=self.cores["primaria_claro"]
        )
        self.lbl_modo_valor.pack(anchor="w", pady=(2, 10))
        
        btn_modo = tk.Button(
            frame_status,
            text="Alternar Modo",
            command=self.alternar_modo,
            bg=self.cores["primaria"],
            fg=self.cores["branco"],
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            activebackground=self.cores["primaria_escuro"],
            activeforeground=self.cores["branco"]
        )
        btn_modo.pack(anchor="w", pady=(0, 15))
        
        # Separador
        self._criar_separador_lateral()
        
        # Estatísticas rápidas
        frame_stats = tk.Frame(self.frame_lateral, bg=self.cores["bg_lateral"])
        frame_stats.pack(fill="x", padx=20, pady=10)
        
        lbl_stats = tk.Label(
            frame_stats,
            text="📊 Estatísticas",
            font=("Segoe UI", 10, "bold"),
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_claro"]
        )
        lbl_stats.pack(anchor="w")
        
        self.lbl_stats_topicos = tk.Label(
            frame_stats,
            text="Carregando...",
            font=("Segoe UI", 9),
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_medio"]
        )
        self.lbl_stats_topicos.pack(anchor="w", pady=2)
        
        self.lbl_stats_fontes = tk.Label(
            frame_stats,
            text="Carregando...",
            font=("Segoe UI", 9),
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_medio"]
        )
        self.lbl_stats_fontes.pack(anchor="w", pady=2)
        
        self._atualizar_estatisticas()
        
        # Separador
        self._criar_separador_lateral()
        
        # Botões de ação
        frame_botoes = tk.Frame(self.frame_lateral, bg=self.cores["bg_lateral"])
        frame_botoes.pack(fill="x", padx=20, pady=10)
        
        btn_stats = tk.Button(
            frame_botoes,
            text="📈 Estatísticas",
            command=self.mostrar_estatisticas,
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_claro"],
            font=("Segoe UI", 9),
            bd=1,
            relief="solid",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        btn_stats.pack(fill="x", pady=5)
        
        btn_ajuda = tk.Button(
            frame_botoes,
            text="❓ Ajuda",
            command=self.mostrar_ajuda,
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_claro"],
            font=("Segoe UI", 9),
            bd=1,
            relief="solid",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        btn_ajuda.pack(fill="x", pady=5)
        
        btn_limpar = tk.Button(
            frame_botoes,
            text="🗑️ Limpar Chat",
            command=self.limpar_chat,
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_claro"],
            font=("Segoe UI", 9),
            bd=1,
            relief="solid",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        btn_limpar.pack(fill="x", pady=5)
        
        # Rodapé
        frame_footer = tk.Frame(self.frame_lateral, bg=self.cores["bg_lateral"])
        frame_footer.pack(side="bottom", fill="x", pady=20)
        
        lbl_footer = tk.Label(
            frame_footer,
            text="v3.0 | Fontes oficiais",
            font=("Segoe UI", 8),
            bg=self.cores["bg_lateral"],
            fg=self.cores["cinza_medio"]
        )
        lbl_footer.pack()
    
    def criar_area_principal(self):
        """Cria área principal do chat"""
        
        self.frame_principal_area = tk.Frame(
            self.frame_principal,
            bg=self.cores["bg_principal"]
        )
        self.frame_principal_area.pack(side="right", fill="both", expand=True)
        
        # Cabeçalho
        frame_header = tk.Frame(
            self.frame_principal_area,
            bg=self.cores["branco"],
            height=70
        )
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        lbl_header = tk.Label(
            frame_header,
            text="💬 Conversa com MozAssist",
            font=("Segoe UI", 16, "bold"),
            bg=self.cores["branco"],
            fg=self.cores["bg_lateral"]
        )
        lbl_header.pack(side="left", padx=25, pady=20)
        
        lbl_online = tk.Label(
            frame_header,
            text="🟢 Online",
            font=("Segoe UI", 9),
            bg=self.cores["branco"],
            fg=self.cores["sucesso"]
        )
        lbl_online.pack(side="right", padx=25, pady=25)
        
        # Área do chat (scrolledtext tradicional)
        self.chat = scrolledtext.ScrolledText(
            self.frame_principal_area,
            height=18,
            width=80,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            bg=self.cores["branco"],
            bd=0,
            relief="flat"
        )
        self.chat.pack(fill="both", expand=True, padx=20, pady=(10, 5))
        
        # Configurar tags para formatação
        self.chat.tag_config("usuario", foreground=self.cores["texto_usuario"], 
                            font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("bot", foreground=self.cores["primaria"], 
                            font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("info", foreground=self.cores["cinza_medio"], 
                            font=("Segoe UI", 9, "italic"))
        self.chat.tag_config("hora", foreground=self.cores["cinza_medio"], 
                            font=("Segoe UI", 8))
        
        # Área de entrada
        frame_entrada = tk.Frame(self.frame_principal_area, bg=self.cores["branco"], height=100)
        frame_entrada.pack(fill="x", side="bottom", padx=20, pady=15)
        frame_entrada.pack_propagate(False)
        
        # Campo de entrada
        self.entrada = tk.Text(
            frame_entrada,
            height=3,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            relief="flat",
            bd=1,
            padx=10,
            pady=8
        )
        self.entrada.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.entrada.bind('<Return>', self.enviar_mensagem)
        self.entrada.bind('<Control-Return>', self.enviar_mensagem)
        
        # Botão enviar
        btn_enviar = tk.Button(
            frame_entrada,
            text="📤 Enviar",
            command=self.enviar_mensagem,
            bg=self.cores["primaria"],
            fg=self.cores["branco"],
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=10,
            bd=0,
            cursor="hand2"
        )
        btn_enviar.pack(side="right")
        
        # Barra de sugestões
        frame_sugestoes = tk.Frame(self.frame_principal_area, bg=self.cores["bg_principal"])
        frame_sugestoes.pack(fill="x", padx=20, pady=(0, 10))
        
        lbl_sugestoes = tk.Label(
            frame_sugestoes,
            text="💡 Sugestões: ",
            font=("Segoe UI", 9),
            bg=self.cores["bg_principal"],
            fg=self.cores["cinza_escuro"]
        )
        lbl_sugestoes.pack(side="left")
        
        sugestoes = ["capital", "províncias", "praias", "gastronomia", "presidente"]
        for sug in sugestoes:
            btn_sug = tk.Button(
                frame_sugestoes,
                text=f"🔹 {sug}",
                command=lambda s=sug: self.usar_sugestao(s),
                bg=self.cores["cinza_claro"],
                fg=self.cores["cinza_escuro"],
                font=("Segoe UI", 8),
                bd=0,
                padx=8,
                pady=3,
                cursor="hand2"
            )
            btn_sug.pack(side="left", padx=3)
    
    def _criar_separador_lateral(self):
        """Cria separador na barra lateral"""
        separator = tk.Frame(
            self.frame_lateral,
            bg=self.cores["primaria_escuro"],
            height=1
        )
        separator.pack(fill="x", padx=20, pady=10)
    
    def _atualizar_estatisticas(self):
        """Atualiza estatísticas na barra lateral"""
        try:
            stats = self.responder.obter_estatisticas()
            self.lbl_stats_topicos.config(text=f"📚 Tópicos: {stats.get('topicos_locais', 0)}")
            self.lbl_stats_fontes.config(text=f"🗂️ Fontes: {stats.get('fontes_configuradas', 0)}")
        except:
            self.lbl_stats_topicos.config(text="📚 Tópicos: --")
            self.lbl_stats_fontes.config(text="🗂️ Fontes: --")
    
    def mostrar_boas_vindas(self):
        """Mostra mensagem de boas-vindas"""
        self.chat.insert(tk.END, "🤖 MozAssist Pro: ", "bot")
        
        boas_vindas = """
Bem-vindo ao MozAssist Pro! 🇲🇿

Sou um assistente especializado em Moçambique, com acesso a fontes confiáveis:
✅ Portais do Governo (.gov.mz)
✅ Televisão de Moçambique (TVM)
✅ Rádio Moçambique (RM)
✅ Jornal Notícias
✅ Instituto Nacional de Estatística (INE)
✅ Banco de Moçambique

🔍 **Como posso ajudar?**
• Perguntas sobre geografia, história e cultura
• Dados estatísticos oficiais
• Informações governamentais
• Turismo e gastronomia

💡 **Dica:** Pressione Enter para enviar mensagem!

O que gostarias de saber sobre Moçambique?
"""
        self.chat.insert(tk.END, boas_vindas)
        self.chat.insert(tk.END, "\n" + "="*60 + "\n\n")
        self.chat.see(tk.END)
    
    def enviar_mensagem(self, event=None):
        """Envia mensagem e processa resposta"""
        pergunta = self.entrada.get("1.0", tk.END).strip()
        
        if pergunta:
            # Mostrar pergunta com hora
            hora = datetime.now().strftime("%H:%M")
            self.chat.insert(tk.END, "\n👤 Você ", "usuario")
            self.chat.insert(tk.END, f"({hora}): ", "hora")
            self.chat.insert(tk.END, f"{pergunta}\n\n")
            self.chat.see(tk.END)
            
            # Limpar entrada
            self.entrada.delete("1.0", tk.END)
            
            # Mostrar indicador
            self.chat.insert(tk.END, "🤖 MozAssist Pro: ", "bot")
            self.chat.insert(tk.END, "🔍 Pesquisando em fontes confiáveis...\n")
            self.chat.see(tk.END)
            self.janela.update()
            
            # Processar em thread separada
            def processar():
                try:
                    resposta = self.responder.gerar_resposta(pergunta)
                    self.janela.after(0, lambda: self.mostrar_resposta(resposta))
                except Exception as e:
                    self.janela.after(0, lambda: self.mostrar_resposta(f"❌ Erro: {str(e)}"))
            
            threading.Thread(target=processar, daemon=True).start()

            return "break"
    
    def mostrar_resposta(self, resposta):
        """Mostra resposta no chat"""
        # Remover indicador de processamento
        ultima_linha = self.chat.get("end-2l", "end-1l")
        if "Pesquisando em fontes confiáveis..." in ultima_linha:
            self.chat.delete("end-2l", "end-1l")
        
        hora = datetime.now().strftime("%H:%M")
        self.chat.insert(tk.END, "🤖 MozAssist Pro ", "bot")
        self.chat.insert(tk.END, f"({hora}):\n", "hora")
        self.chat.insert(tk.END, f"{resposta}\n\n")
        self.chat.insert(tk.END, "-"*60 + "\n\n")
        self.chat.see(tk.END)
        self.entrada.focus()
    
    def limpar_chat(self):
        """Limpa o chat"""
        self.chat.delete(1.0, tk.END)
        self.mostrar_boas_vindas()
    
    def alternar_modo(self):
        """Alterna modo de busca"""
        msg = self.responder.alternar_modo_busca()
        self.lbl_modo_valor.config(text=self.responder.modo_busca.upper())
        
        self.chat.insert(tk.END, "ℹ️ Sistema: ", "info")
        self.chat.insert(tk.END, f"{msg}\n\n")
        self.chat.see(tk.END)
        self._atualizar_estatisticas()
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas do sistema"""
        stats = self.responder.obter_estatisticas()
        
        mensagem = f"""
📊 **Estatísticas do MozAssist Pro:**

• 🌐 Modo de busca: {stats.get('modo_busca', 'N/A').upper()}
• 📚 Tópicos locais: {stats.get('topicos_locais', 0)}
• 🔍 Buscas realizadas: {stats.get('buscas_realizadas', 0)}
• 🗂️ Fontes configuradas: {stats.get('fontes_configuradas', 0)}

💡 Dica: Use "alternar modo" para mudar entre busca local e híbrida!
"""
        self.chat.insert(tk.END, "📊 MozAssist Pro: ", "bot")
        self.chat.insert(tk.END, mensagem + "\n")
        self.chat.see(tk.END)
    
    def mostrar_ajuda(self):
        """Mostra ajuda"""
        ajuda = """
        🤖 **MozAssist Pro - Guia Rápido**
        
        📝 **O que posso fazer:**
        
        • **Perguntas sobre Moçambique**
          Ex: "Qual é a capital?", "Quais são as províncias?"
        
        • **Dados estatísticos**
          Ex: "Quantos médicos tem Moçambique?"
        
        • **Informações governamentais**
          Ex: "Quem é o presidente?", "Ministros do governo"
        
        • **Cultura e turismo**
          Ex: "Gastronomia típica", "Praias de Moçambique"
        
        🔧 **Comandos especiais:**
        • **alternar modo** - Troca entre local/híbrido
        • **estatísticas** - Mostra dados do sistema
        • **ajuda** - Mostra esta mensagem
        
        🌐 **Fontes utilizadas:**
        🏛️ Portais do Governo (.gov.mz)
        📊 INE, Banco de Moçambique
        📺 TVM, RM, Jornal Notícias
        """
        self.chat.insert(tk.END, "❓ MozAssist Pro: ", "bot")
        self.chat.insert(tk.END, ajuda + "\n")
        self.chat.see(tk.END)
    
    def usar_sugestao(self, sugestao):
        """Usa uma sugestão de pergunta"""
        self.entrada.delete("1.0", tk.END)
        self.entrada.insert("1.0", sugestao)
        self.enviar_mensagem()
    
    def iniciar(self):
        """Inicia a aplicação"""
        self.janela.mainloop()
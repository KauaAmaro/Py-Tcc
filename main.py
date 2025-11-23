#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from database import Database
from barcode_reader import BarcodeReader
from report_generator import ReportGenerator

class BarcodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leitor de Códigos de Barras")
        self.root.geometry("600x400")
        
        self.db = Database()
        self.reader = BarcodeReader()
        self.reader.set_callback(self.on_barcode_read)
        self.report_gen = ReportGenerator(self.db)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Leitor de Códigos de Barras", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Botões principais
        self.start_button = ttk.Button(main_frame, text="Iniciar Leitura", 
                                      command=self.toggle_reading)
        self.start_button.grid(row=1, column=0, padx=(0, 10), pady=5, sticky=tk.W+tk.E)
        
        cadastro_button = ttk.Button(main_frame, text="Cadastrar Produto", 
                                   command=self.open_cadastro)
        cadastro_button.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W+tk.E)
        
        stats_button = ttk.Button(main_frame, text="Ver Estatísticas", 
                                command=self.show_stats)
        stats_button.grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        
        reports_button = ttk.Button(main_frame, text="Gerar Relatórios", 
                                  command=self.open_reports)
        reports_button.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Status: Parado", 
                                     foreground="red")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(20, 10))
        
        # Log de leituras
        log_label = ttk.Label(main_frame, text="Log de Leituras:")
        log_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # Frame para o log com scrollbar
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def toggle_reading(self):
        if self.reader.is_running():
            self.reader.stop_reading()
            self.start_button.config(text="Iniciar Leitura")
            self.status_label.config(text="Status: Parado", foreground="red")
            self.log_message("Leitura parada")
        else:
            if self.reader.start_reading():
                self.start_button.config(text="Parar Leitura")
                self.status_label.config(text="Status: Lendo", foreground="green")
                self.log_message("Leitura iniciada")
            else:
                messagebox.showerror("Erro", "Não foi possível conectar à câmera IP")
    
    def open_cadastro(self):
        CadastroWindow(self.root, self.db)
    
    def open_reports(self):
        ReportsWindow(self.root, self.report_gen)
    
    def show_stats(self):
        stats = self.db.get_leituras_stats()
        if not stats:
            messagebox.showinfo("Estatísticas", "Nenhuma leitura registrada ainda")
            return
        
        StatsWindow(self.root, stats)
    
    def on_barcode_read(self, message, msg_type):
        self.root.after(0, lambda: self.log_message(message, msg_type))
    
    def log_message(self, message, msg_type="info"):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
        # Colorir mensagens por tipo
        if msg_type == "success":
            self.log_text.tag_add("success", "end-2l", "end-1l")
            self.log_text.tag_config("success", foreground="green")
        elif msg_type == "warning":
            self.log_text.tag_add("warning", "end-2l", "end-1l")
            self.log_text.tag_config("warning", foreground="orange")
        elif msg_type == "error":
            self.log_text.tag_add("error", "end-2l", "end-1l")
            self.log_text.tag_config("error", foreground="red")

class CadastroWindow:
    def __init__(self, parent, db):
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title("Cadastro de Produtos")
        self.window.geometry("400x300")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        self.load_produtos()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Formulário
        ttk.Label(main_frame, text="Código de Barras:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.codigo_entry = ttk.Entry(main_frame, width=30)
        self.codigo_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        ttk.Label(main_frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.descricao_entry = ttk.Entry(main_frame, width=30)
        self.descricao_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        ttk.Button(main_frame, text="Cadastrar", command=self.cadastrar).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Lista de produtos
        ttk.Label(main_frame, text="Produtos Cadastrados:").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        # Treeview para lista
        self.tree = ttk.Treeview(main_frame, columns=("codigo", "descricao"), show="headings", height=6)
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")
        self.tree.column("codigo", width=150)
        self.tree.column("descricao", width=200)
        self.tree.grid(row=4, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botões de ação
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Editar", command=self.editar_produto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Deletar", command=self.deletar_produto).pack(side=tk.LEFT, padx=5)
        
        # Scrollbar para treeview
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=4, column=2, sticky=(tk.N, tk.S))
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def cadastrar(self):
        codigo = self.codigo_entry.get().strip()
        descricao = self.descricao_entry.get().strip()
        
        if not codigo:
            messagebox.showerror("Erro", "Código de barras é obrigatório")
            return
        
        if self.db.add_produto(codigo, descricao):
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
            self.codigo_entry.delete(0, tk.END)
            self.descricao_entry.delete(0, tk.END)
            self.load_produtos()
        else:
            messagebox.showerror("Erro", "Código já cadastrado")
    
    def load_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        produtos = self.db.get_produtos()
        for codigo, descricao in produtos:
            self.tree.insert("", tk.END, values=(codigo, descricao or "Sem descrição"))
    
    def editar_produto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto para editar")
            return
        
        item = self.tree.item(selected[0])
        codigo_atual, descricao_atual = item['values']
        
        # Janela de edição
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Editar Produto")
        edit_window.geometry("300x150")
        edit_window.transient(self.window)
        edit_window.grab_set()
        
        ttk.Label(edit_window, text="Código:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        codigo_entry = ttk.Entry(edit_window, width=25)
        codigo_entry.insert(0, codigo_atual)
        codigo_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Descrição:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        desc_entry = ttk.Entry(edit_window, width=25)
        desc_entry.insert(0, descricao_atual if descricao_atual != "Sem descrição" else "")
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def salvar():
            novo_codigo = codigo_entry.get().strip()
            nova_desc = desc_entry.get().strip()
            
            if not novo_codigo:
                messagebox.showerror("Erro", "Código é obrigatório")
                return
            
            if self.db.update_produto(codigo_atual, novo_codigo, nova_desc):
                messagebox.showinfo("Sucesso", "Produto atualizado")
                edit_window.destroy()
                self.load_produtos()
            else:
                messagebox.showerror("Erro", "Código já existe")
        
        ttk.Button(edit_window, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2, pady=10)
    
    def deletar_produto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto para deletar")
            return
        
        item = self.tree.item(selected[0])
        codigo = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Deletar produto {codigo}?\nTodas as leituras serão removidas."):
            self.db.delete_produto(codigo)
            messagebox.showinfo("Sucesso", "Produto deletado")
            self.load_produtos()

class StatsWindow:
    def __init__(self, parent, stats):
        self.window = tk.Toplevel(parent)
        self.window.title("Estatísticas de Leitura")
        self.window.geometry("800x600")
        self.window.transient(parent)
        
        self.create_chart(stats)
    
    def create_chart(self, stats):
        # Preparar dados
        codigos = [row[0] for row in stats]
        leituras = [row[2] for row in stats]
        
        # Criar gráfico de colunas verticais
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.bar(range(len(codigos)), leituras, color='steelblue', edgecolor='darkblue', width=0.6)
        
        # Configurar eixos
        ax.set_xlabel('Códigos de Barras', fontsize=12)
        ax.set_ylabel('Quantidade de Leituras', fontsize=12)
        ax.set_title('Estatísticas de Leitura por Código', fontsize=14, fontweight='bold')
        
        # Configurar labels do eixo X
        ax.set_xticks(range(len(codigos)))
        ax.set_xticklabels(codigos, rotation=45, ha='right')
        
        # Adicionar valores no topo das colunas
        for i, (bar, value) in enumerate(zip(bars, leituras)):
            ax.text(i, value + 0.1, str(value), ha='center', va='bottom', fontweight='bold')
        
        # Ajustar grid
        ax.grid(axis='y', alpha=0.3)
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        
        # Integrar com Tkinter
        canvas = FigureCanvasTkAgg(fig, self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

class ReportsWindow:
    def __init__(self, parent, report_gen):
        self.report_gen = report_gen
        self.window = tk.Toplevel(parent)
        self.window.title("Gerar Relatórios")
        self.window.geometry("400x300")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Gerar Relatórios", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Seleção de período
        period_frame = ttk.LabelFrame(main_frame, text="Período", padding="10")
        period_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.period_var = tk.StringVar(value="dia")
        ttk.Radiobutton(period_frame, text="Dia específico", variable=self.period_var, value="dia").pack(anchor=tk.W)
        ttk.Radiobutton(period_frame, text="Mês inteiro", variable=self.period_var, value="mes").pack(anchor=tk.W)
        
        # Data
        date_frame = ttk.LabelFrame(main_frame, text="Data", padding="10")
        date_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(date_frame, text="Data (AAAA-MM-DD):").pack(anchor=tk.W)
        self.date_entry = ttk.Entry(date_frame, width=15)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(anchor=tk.W, pady=(5, 0))
        
        ttk.Label(date_frame, text="Mês/Ano (MM/AAAA):").pack(anchor=tk.W, pady=(10, 0))
        self.month_entry = ttk.Entry(date_frame, width=15)
        self.month_entry.insert(0, datetime.now().strftime("%m/%Y"))
        self.month_entry.pack(anchor=tk.W, pady=(5, 0))
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Gerar Excel", command=self.gerar_excel).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Gerar PDF", command=self.gerar_pdf).pack(side=tk.LEFT)
    
    def gerar_excel(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if not filename:
                return
            
            if self.period_var.get() == "dia":
                data = self.date_entry.get()
                success = self.report_gen.gerar_planilha_dia(data, filename)
            else:
                mes_ano = self.month_entry.get().split("/")
                mes, ano = int(mes_ano[0]), int(mes_ano[1])
                success = self.report_gen.gerar_planilha_mes(ano, mes, filename)
            
            if success:
                messagebox.showinfo("Sucesso", "Planilha gerada com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Nenhum dado encontrado para o período selecionado")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar planilha: {str(e)}")
    
    def gerar_pdf(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not filename:
                return
            
            if self.period_var.get() == "dia":
                data = self.date_entry.get()
                success = self.report_gen.gerar_pdf_dia(data, filename)
            else:
                mes_ano = self.month_entry.get().split("/")
                mes, ano = int(mes_ano[0]), int(mes_ano[1])
                success = self.report_gen.gerar_pdf_mes(ano, mes, filename)
            
            if success:
                messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Nenhum dado encontrado para o período selecionado")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")

def main():
    root = tk.Tk()
    app = BarcodeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
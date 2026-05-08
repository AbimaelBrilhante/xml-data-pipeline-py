import tkinter as tk
from tkinter import filedialog, messagebox
import main_events
import os

class FiscalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação Fiscal XML v2.0")
        self.root.geometry("500x350")
        self.root.configure(bg="#f0f0f0")

        # Variáveis de caminho
        self.input_folder = tk.StringVar()
        self.db_path = "data/fiscal_data.db"

        self.setup_ui()

    def setup_ui(self):
        """Configura os elementos visuais da janela."""
        title = tk.Label(self.root, text="Pipeline de Dados Fiscais", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=20)

        # Seleção de Pasta
        frame_folder = tk.Frame(self.root, bg="#f0f0f0")
        frame_folder.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_folder, text="Pasta de XMLs:", bg="#f0f0f0").pack(side="left")
        entry_path = tk.Entry(frame_folder, textvariable=self.input_folder, state="readonly")
        entry_path.pack(side="left", expand=True, fill="x", padx=5)
        
        btn_browse = tk.Button(frame_folder, text="Selecionar", command=self.browse_folder)
        btn_browse.pack(side="right")

        # Botões de Ação
        self.btn_process = tk.Button(self.root, text="🚀 Processar XMLs", command=self.run_process, 
                                     bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), height=2)
        self.btn_process.pack(pady=10, padx=20, fill="x")

        self.btn_export = tk.Button(self.root, text="📊 Gerar Relatório Excel", command=self.run_export, 
                                     bg="#3498db", fg="white", font=("Arial", 10, "bold"), height=2)
        self.btn_export.pack(pady=10, padx=20, fill="x")

        # Rodapé
        self.status_label = tk.Label(self.root, text="Pronto para iniciar.", bg="#f0f0f0", fg="#777")
        self.status_label.pack(side="bottom", pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)

    def run_process(self):
        folder = self.input_folder.get()
        if not folder:
            messagebox.showwarning("Aviso", "Por favor, selecione a pasta de XMLs primeiro.")
            return

        try:
            self.status_label.config(text="A processar... Por favor, aguarde.", fg="blue")
            self.root.update_idletasks()
            
            # Garante que a pasta 'data' existe para o BD
            os.makedirs("data", exist_ok=True)
            
            main_events.process_all_xmls(folder, self.db_path)
            
            messagebox.showinfo("Sucesso", "Processamento concluído e dados gravados no banco!")
            self.status_label.config(text="Processamento finalizado.", fg="green")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
            self.status_label.config(text="Erro no processamento.", fg="red")

    def run_export(self):
        if not os.path.exists(self.db_path):
            messagebox.showwarning("Erro", "Banco de dados não encontrado. Processe os XMLs primeiro.")
            return
        
        output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                   filetypes=[("Excel files", "*.xlsx")])
        if output_file:
            main_events.export_results_to_excel(self.db_path, output_file)
            messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{output_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FiscalApp(root)
    root.mainloop()

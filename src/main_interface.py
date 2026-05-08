import customtkinter as ctk
from tkinter import filedialog, messagebox
import main_events
import os

# Configuração de aparência (Pode ser "System", "Dark" ou "Light")
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FiscalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fiscal XML Pipeline v2.0")
        self.geometry("600x450")

        # Variáveis
        self.input_folder = ctk.StringVar()
        self.db_path = "data/fiscal_data.db"

        self.setup_ui()

    def setup_ui(self):
        # Frame Principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_title = ctk.CTkLabel(self.main_frame, text="Fiscal Data Pipeline",
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.pack(pady=20)

        # Seleção de Pasta
        self.folder_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.folder_frame.pack(pady=10, padx=30, fill="x")

        self.entry_path = ctk.CTkEntry(self.folder_frame, placeholder_text="Caminho da pasta...",
                                       textvariable=self.input_folder, width=350)
        self.entry_path.pack(side="left", padx=(0, 10))

        self.btn_browse = ctk.CTkButton(self.folder_frame, text="Selecionar", width=100,
                                        command=self.browse_folder)
        self.btn_browse.pack(side="right")

        # Botões de Ação com ícones (Simulados por estilo)
        self.btn_process = ctk.CTkButton(self.main_frame, text="🚀  PROCESSAR XMLs",
                                         command=self.run_process,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         fg_color="#2ecc71", hover_color="#27ae60",
                                         height=50)
        self.btn_process.pack(pady=15, padx=60, fill="x")

        self.btn_export = ctk.CTkButton(self.main_frame, text="📊  GERAR RELATÓRIO EXCEL",
                                        command=self.run_export,
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        height=50)
        self.btn_export.pack(pady=15, padx=60, fill="x")

        # Barra de Status
        self.status_label = ctk.CTkLabel(self.main_frame, text="Status: Aguardando seleção",
                                         text_color="gray")
        self.status_label.pack(side="bottom", pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)
            self.status_label.configure(text=f"Pasta selecionada: {os.path.basename(folder)}", text_color="white")

    def run_process(self):
        folder = self.input_folder.get()
        if not folder:
            messagebox.showwarning("Aviso", "Por favor, selecione a pasta primeiro.")
            return

        self.status_label.configure(text="Processando... Aguarde.", text_color="#f1c40f")
        self.update()

        try:
            os.makedirs("data", exist_ok=True)
            main_events.process_all_xmls(folder, self.db_path)
            messagebox.showinfo("Sucesso", "Dados processados e salvos com sucesso!")
            self.status_label.configure(text="Processamento Finalizado!", text_color="#2ecc71")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.status_label.configure(text="Erro no processamento", text_color="#e74c3c")

    def run_export(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Excel files", "*.xlsx")])
        if output_file:
            main_events.export_results_to_excel(self.db_path, output_file)
            messagebox.showinfo("Sucesso", "Excel gerado com sucesso!")


if __name__ == "__main__":
    app = FiscalApp()
    app.mainloop()

"""
FISCAL XML DATA PIPELINE - ENTRY POINT
Author: Abimael Brilhante
Description: Main script to launch the Fiscal Automation GUI.
"""
import sys
import os

# Adiciona a pasta 'src' ao caminho do sistema para evitar erros de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main_interface import FiscalApp
import tkinter as tk
import logging

# Configuração de Logs para monitoramento do sistema
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data/system_log.log"),
        logging.StreamHandler()
    ]
)

def main():
    try:
        logging.info("Starting Fiscal Automation System...")
        root = tk.Tk()
        app = FiscalApp(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"System failed to start: {e}")

if __name__ == "__main__":
    main()

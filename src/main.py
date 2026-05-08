"""
FISCAL XML DATA PIPELINE - ENTRY POINT
Author: Abimael Brilhante
Description: Main script to launch the Fiscal Automation GUI.
"""
import sys
import os
import logging

# Adiciona a pasta raiz ao caminho para garantir que os módulos sejam encontrados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a classe da nova interface moderna
from src.main_interface import FiscalApp

# Configuração de Logs (MANTENHA ISSO)
if not os.path.exists("data"):
    os.makedirs("data")

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
        # Inicialização simplificada para CustomTkinter
        app = FiscalApp() 
        app.mainloop()
    except Exception as e:
        logging.critical(f"System failed to start: {e}")

if __name__ == "__main__":
    main()

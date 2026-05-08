import pandas as pd
import sqlite3
import os
import logging
from xml_parser import XMLParser
from database_manager import DataBaseManager

# Configuração básica de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_all_xmls(input_directory, db_path):
    """
    Orquestra a leitura, extração e gravação dos dados.
    """
    parser = XMLParser(input_directory)
    db = DataBaseManager(db_path)
    
    all_files = parser.all_files()
    nfe_data_list = []
    cte_data_list = []

    logging.info(f"Iniciando processamento de {len(all_files)} ficheiros...")

    for file_path in all_files:
        # Tenta ler como NF-e primeiro
        nfe = parser.parse_nfe(file_path)
        if nfe:
            nfe_data_list.append(nfe)
            continue
        
        # Se não for NF-e, tenta ler como CT-e
        cte = parser.parse_cte(file_path)
        if cte:
            cte_data_list.append(cte)

    # Gravação no Banco de Dados
    if nfe_data_list:
        db.insert_invoices(nfe_data_list)
        logging.info(f"{len(nfe_data_list)} NF-e gravadas com sucesso.")

    if cte_data_list:
        db.insert_freights(cte_data_list)
        logging.info(f"{len(cte_data_list)} CT-e gravados com sucesso.")

    db.close()

def export_results_to_excel(db_path, output_excel_path):
    """
    Lê os dados do SQLite e exporta para um ficheiro Excel.
    """
    try:
        conn = sqlite3.connect(db_path)
        
        # Criando um ficheiro Excel com duas abas (Notas e Fretes)
        with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
            df_nfe = pd.read_sql_query("SELECT * FROM Invoices", conn)
            df_nfe.to_excel(writer, sheet_name='Notas Fiscais', index=False)
            
            df_cte = pd.read_sql_query("SELECT * FROM Freights", conn)
            df_cte.to_excel(writer, sheet_name='Fretes (CTe)', index=False)
            
        conn.close()
        logging.info(f"Relatório exportado para: {output_excel_path}")
    except Exception as e:
        logging.error(f"Erro ao exportar para Excel: {e}")

def clear_input_folder(directory):
    """
    Opcional: Limpa a pasta de entrada após o processamento (baseado no teu código tumba_manual).
    """
    for f in os.listdir(directory):
        file_path = os.path.join(directory, f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            logging.error(f"Erro ao apagar {file_path}: {e}")

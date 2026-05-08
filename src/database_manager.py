import sqlite3
import logging

class DataBaseManager:
    """
    Classe responsável por gerenciar todas as operações de banco de dados SQLite.
    Centraliza a criação de tabelas e a inserção de dados para NFe e CTe.
    """
    def __init__(self, db_path="data/fiscal_reports.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        """Cria as tabelas de Notas e Fretes caso não existam."""
        cursor = self.connection.cursor()
        
        # Tabela de Notas Fiscais (NFe)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Invoices (
                invoice_number TEXT,
                serie TEXT,
                issue_date TEXT,
                access_key TEXT PRIMARY KEY,
                issuer_cnpj TEXT,
                issuer_name TEXT,
                dest_cnpj TEXT,
                total_value REAL,
                status TEXT
            );
        """)

        # Tabela de Fretes (CTe)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Freights (
                cte_number TEXT,
                serie TEXT,
                issue_date TEXT,
                access_key TEXT PRIMARY KEY,
                issuer_cnpj TEXT,
                issuer_name TEXT,
                total_amount REAL,
                status TEXT
            );
        """)
        self.connection.commit()

    def insert_invoices(self, invoices_data):
        """Insere uma lista de tuplas com dados de NFe."""
        cursor = self.connection.cursor()
        query = "INSERT OR IGNORE INTO Invoices VALUES (?,?,?,?,?,?,?,?,?)"
        cursor.executemany(query, invoices_data)
        self.connection.commit()

    def insert_freights(self, freights_data):
        """Insere uma lista de tuplas com dados de CTe."""
        cursor = self.connection.cursor()
        query = "INSERT OR IGNORE INTO Freights VALUES (?,?,?,?,?,?,?,?)"
        cursor.executemany(query, freights_data)
        self.connection.commit()

    def close(self):
        """Encerra a conexão com o banco de dados."""
        self.connection.close()

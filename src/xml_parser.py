import os
import xml.etree.ElementTree as ET
import zipfile
import logging

class XMLParser:
    """
    Classe responsável por navegar nos ficheiros XML (NF-e e CT-e),
    tratar namespaces e extrair os dados fiscais de forma estruturada.
    """
    def __init__(self, directory):
        self.directory = directory
        # Namespaces padrão da SEFAZ
        self.ns_nfe = {"ns": "http://www.portalfiscal.inf.br/nfe"}
        self.ns_cte = {"ns": "http://www.portalfiscal.inf.br/cte"}

    def all_files(self):
        """Lista ficheiros XML e extrai conteúdos de ficheiros ZIP."""
        xml_files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) 
                     if f.lower().endswith(".xml")]
        
        zip_files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) 
                     if f.lower().endswith(".zip")]

        for zip_file in zip_files:
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(self.directory)
                    xml_files.extend([os.path.join(self.directory, f) for f in zip_ref.namelist() 
                                      if f.lower().endswith(".xml")])
            except Exception as e:
                logging.error(f"Erro ao extrair ZIP {zip_file}: {e}")

        return xml_files

    def parse_nfe(self, xml_path):
        """Extrai dados de uma NF-e."""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Helper para extrair texto de forma segura
            def get_txt(path):
                node = root.find(path, self.ns_nfe)
                return node.text if node is not None else ""

            # Mapeamento baseado no teu código original
            data = (
                get_txt(".//ns:ide/ns:nNF"),            # Numero
                get_txt(".//ns:ide/ns:serie"),          # Serie
                get_txt(".//ns:ide/ns:dhEmi"),          # Data Emissão
                get_txt(".//ns:infNFe").attrib['Id'][3:], # Chave (remove 'NFe')
                get_txt(".//ns:emit/ns:CNPJ"),          # CNPJ Emitente
                get_txt(".//ns:emit/ns:xNome"),         # Nome Emitente
                get_txt(".//ns:dest/ns:CNPJ") or get_txt(".//ns:dest/ns:CPF"), # Destinatário
                float(get_txt(".//ns:vNF") or 0),       # Valor Total
                "Processado"                            # Status
            )
            return data
        except Exception as e:
            logging.error(f"Falha ao ler NF-e {xml_path}: {e}")
            return None

    def parse_cte(self, xml_path):
        """Extrai dados de um CT-e."""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            def get_txt(path):
                node = root.find(path, self.ns_cte)
                return node.text if node is not None else ""

            data = (
                get_txt(".//ns:ide/ns:cCT"),            # Numero CTe
                get_txt(".//ns:ide/ns:serie"),          # Serie
                get_txt(".//ns:ide/ns:dhEmi"),          # Data Emissão
                get_txt(".//ns:infCte").attrib['Id'][3:], # Chave
                get_txt(".//ns:emit/ns:CNPJ"),          # CNPJ Emitente
                get_txt(".//ns:emit/ns:xNome"),         # Nome Emitente
                float(get_txt(".//ns:vTPrest") or 0),   # Valor Total
                "Processado"                            # Status
            )
            return data
        except Exception as e:
            logging.error(f"Falha ao ler CT-e {xml_path}: {e}")
            return None

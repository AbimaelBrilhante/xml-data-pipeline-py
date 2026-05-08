import os
import xml.etree.ElementTree as ET
import zipfile
import logging

class XMLParser:
    def __init__(self, directory):
        self.directory = directory
        self.ns_nfe = {"ns": "http://www.portalfiscal.inf.br/nfe"}
        self.ns_cte = {"ns": "http://www.portalfiscal.inf.br/cte"}

    def all_files(self):
        xml_files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) 
                     if f.lower().endswith(".xml")]
        return xml_files

    def parse_nfe(self, xml_path):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Localiza o nó da NFe (infNFe)
            infNFe = root.find(".//ns:infNFe", self.ns_nfe)
            if infNFe is None:
                return None # Não é uma NFe válida

            chave = infNFe.attrib.get('Id', '')[3:] # Remove o prefixo 'NFe'

            def get_txt(path):
                node = root.find(path, self.ns_nfe)
                return node.text if node is not None else ""

            data = (
                get_txt(".//ns:ide/ns:nNF"),
                get_txt(".//ns:ide/ns:serie"),
                get_txt(".//ns:ide/ns:dhEmi"),
                chave,
                get_txt(".//ns:emit/ns:CNPJ"),
                get_txt(".//ns:emit/ns:xNome"),
                get_txt(".//ns:dest/ns:CNPJ") or get_txt(".//ns:dest/ns:CPF"),
                float(get_txt(".//ns:total/ns:ICMSTot/ns:vNF") or 0),
                "Processado"
            )
            return data
        except Exception as e:
            logging.error(f"Falha ao ler NF-e {xml_path}: {e}")
            return None

    def parse_cte(self, xml_path):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Localiza o nó do CTe (infCte)
            infCte = root.find(".//ns:infCte", self.ns_cte)
            if infCte is None:
                return None

            chave = infCte.attrib.get('Id', '')[3:] # Remove o prefixo 'CTe'

            def get_txt(path):
                node = root.find(path, self.ns_cte)
                return node.text if node is not None else ""

            data = (
                get_txt(".//ns:ide/ns:cCT"),
                get_txt(".//ns:ide/ns:serie"),
                get_txt(".//ns:ide/ns:dhEmi"),
                chave,
                get_txt(".//ns:emit/ns:CNPJ"),
                get_txt(".//ns:emit/ns:xNome"),
                float(get_txt(".//ns:vPrest/ns:vTPrest") or 0),
                "Processado"
            )
            return data
        except Exception as e:
            logging.error(f"Falha ao ler CT-e {xml_path}: {e}")
            return None

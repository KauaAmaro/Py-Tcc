import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="barcode_reader.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabela produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                codigo_barras TEXT PRIMARY KEY,
                descricao TEXT
            )
        ''')
        
        # Tabela leituras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leituras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_barras TEXT,
                data_hora TIMESTAMP,
                FOREIGN KEY (codigo_barras) REFERENCES produtos (codigo_barras)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_produto(self, codigo_barras, descricao=""):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO produtos (codigo_barras, descricao) VALUES (?, ?)", 
                         (codigo_barras, descricao))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def produto_exists(self, codigo_barras):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def add_leitura(self, codigo_barras):
        if self.produto_exists(codigo_barras):
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO leituras (codigo_barras, data_hora) VALUES (?, ?)", 
                         (codigo_barras, datetime.now()))
            conn.commit()
            conn.close()
            return True
        return False
    
    def get_leituras_stats(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.codigo_barras, p.descricao, COUNT(l.id) as total_leituras
            FROM produtos p
            LEFT JOIN leituras l ON p.codigo_barras = l.codigo_barras
            GROUP BY p.codigo_barras, p.descricao
            HAVING total_leituras > 0
            ORDER BY total_leituras DESC
        ''')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_produtos(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT codigo_barras, descricao FROM produtos")
        result = cursor.fetchall()
        conn.close()
        return result
    
    def update_produto(self, codigo_original, novo_codigo, nova_descricao):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE produtos SET codigo_barras = ?, descricao = ? WHERE codigo_barras = ?", 
                         (novo_codigo, nova_descricao, codigo_original))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def delete_produto(self, codigo_barras):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leituras WHERE codigo_barras = ?", (codigo_barras,))
        cursor.execute("DELETE FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
        conn.commit()
        conn.close()
    
    def get_leituras_por_dia(self, data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.codigo_barras, p.descricao, l.data_hora
            FROM leituras l
            JOIN produtos p ON l.codigo_barras = p.codigo_barras
            WHERE DATE(l.data_hora) = ?
            ORDER BY l.data_hora
        ''', (data,))
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_leituras_por_mes(self, ano, mes):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.codigo_barras, p.descricao, l.data_hora
            FROM leituras l
            JOIN produtos p ON l.codigo_barras = p.codigo_barras
            WHERE strftime('%Y', l.data_hora) = ? AND strftime('%m', l.data_hora) = ?
            ORDER BY l.data_hora
        ''', (str(ano), f"{mes:02d}"))
        result = cursor.fetchall()
        conn.close()
        return result
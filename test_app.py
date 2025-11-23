#!/usr/bin/env python3
"""Script de teste para verificar funcionamento básico do aplicativo"""

from database import Database
import os

def test_database():
    """Testa funcionalidades básicas do banco de dados"""
    print("Testando banco de dados...")
    
    # Criar instância do banco
    db = Database("test.db")
    
    # Testar cadastro de produto
    result = db.add_produto("123456789", "Produto Teste")
    print(f"Cadastro de produto: {'OK' if result else 'ERRO'}")
    
    # Testar verificação de existência
    exists = db.produto_exists("123456789")
    print(f"Produto existe: {'OK' if exists else 'ERRO'}")
    
    # Testar registro de leitura
    leitura_ok = db.add_leitura("123456789")
    print(f"Registro de leitura: {'OK' if leitura_ok else 'ERRO'}")
    
    # Testar estatísticas
    stats = db.get_leituras_stats()
    print(f"Estatísticas: {'OK' if len(stats) > 0 else 'ERRO'}")
    
    # Limpar arquivo de teste
    os.remove("test.db")
    print("Teste do banco de dados concluído!")

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("Verificando dependências...")
    
    try:
        import cv2
        print("✓ OpenCV instalado")
    except ImportError:
        print("✗ OpenCV não encontrado - instale com: pip install opencv-python")
    
    try:
        import pyzbar
        print("✓ pyzbar instalado")
    except ImportError:
        print("✗ pyzbar não encontrado - instale com: pip install pyzbar")
    
    try:
        import matplotlib
        print("✓ matplotlib instalado")
    except ImportError:
        print("✗ matplotlib não encontrado - instale com: pip install matplotlib")
    
    try:
        import tkinter
        print("✓ tkinter disponível")
    except ImportError:
        print("✗ tkinter não encontrado - instale tkinter")

if __name__ == "__main__":
    print("=== TESTE DO APLICATIVO LEITOR DE CÓDIGOS DE BARRAS ===\n")
    
    check_dependencies()
    print()
    test_database()
    
    print("\n=== TESTE CONCLUÍDO ===")
    print("Para executar o aplicativo: python main.py")
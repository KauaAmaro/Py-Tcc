import os
import subprocess
import sys

def build_executable():
    """Script para gerar executável com PyInstaller"""
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=BarcodeReader",
        "--add-data=barcode_reader.db:.",
        "main.py"
    ]
    
    print("Gerando executável...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Executável gerado com sucesso!")
        print("Localização: dist/BarcodeReader")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar executável: {e}")
        print(f"Saída do erro: {e.stderr}")
    except FileNotFoundError:
        print("PyInstaller não encontrado. Instale com: pip install pyinstaller")

if __name__ == "__main__":
    build_executable()
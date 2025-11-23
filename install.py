#!/usr/bin/env python3
"""Script de instalação automática das dependências"""

import subprocess
import sys
import os

def install_dependencies():
    """Instala todas as dependências necessárias"""
    print("Instalando dependências do projeto...")
    
    # Lista de pacotes necessários
    packages = [
        "opencv-python==4.8.1.78",
        "pyzbar==0.1.9", 
        "matplotlib==3.7.2",
        "Pillow==10.0.0",
        "pyinstaller==5.13.2"
    ]
    
    for package in packages:
        print(f"Instalando {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} instalado com sucesso")
        except subprocess.CalledProcessError as e:
            print(f"✗ Erro ao instalar {package}: {e}")
            return False
    
    return True

def check_tkinter():
    """Verifica se tkinter está disponível"""
    try:
        import tkinter
        print("✓ tkinter está disponível")
        return True
    except ImportError:
        print("✗ tkinter não encontrado")
        print("No Ubuntu/Debian: sudo apt-get install python3-tk")
        print("No CentOS/RHEL: sudo yum install tkinter")
        return False

def main():
    print("=== INSTALAÇÃO DO LEITOR DE CÓDIGOS DE BARRAS ===\n")
    
    # Verificar tkinter primeiro
    tkinter_ok = check_tkinter()
    
    # Instalar dependências
    deps_ok = install_dependencies()
    
    print("\n=== RESULTADO DA INSTALAÇÃO ===")
    if deps_ok and tkinter_ok:
        print("✓ Instalação concluída com sucesso!")
        print("Execute: python3 main.py")
    else:
        print("✗ Problemas na instalação. Verifique os erros acima.")
        if not tkinter_ok:
            print("Instale tkinter manualmente para sua distribuição Linux")

if __name__ == "__main__":
    main()
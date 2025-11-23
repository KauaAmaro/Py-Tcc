#!/usr/bin/env python3
"""Script de instalação para Debian/Ubuntu sem sudo"""

import subprocess
import sys
import os

def install_with_user_flag():
    """Instala pacotes no diretório do usuário"""
    packages = [
        "opencv-python==4.8.1.78",
        "pyzbar==0.1.9", 
        "matplotlib==3.7.2",
        "Pillow==10.0.0"
    ]
    
    print("Instalando dependências no diretório do usuário...")
    
    for package in packages:
        print(f"Instalando {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--user", "--break-system-packages", package
            ])
            print(f"✓ {package} instalado")
        except subprocess.CalledProcessError as e:
            print(f"✗ Erro ao instalar {package}: {e}")
            return False
    
    return True

def main():
    print("=== INSTALAÇÃO PARA DEBIAN/UBUNTU ===\n")
    
    print("ATENÇÃO: Este sistema precisa de tkinter instalado pelo administrador.")
    print("Execute como root: apt install python3-tk python3-venv\n")
    
    # Tentar instalar dependências
    if install_with_user_flag():
        print("\n✓ Dependências Python instaladas!")
        print("Agora instale tkinter como root: apt install python3-tk")
        print("Depois execute: python3 main.py")
    else:
        print("\n✗ Falha na instalação das dependências")

if __name__ == "__main__":
    main()
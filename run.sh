#!/bin/bash
# Script para executar o aplicativo

echo "Iniciando Leitor de Códigos de Barras..."

# Verificar se Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Instale Python3 primeiro."
    exit 1
fi

# Executar aplicativo
python3 main.py
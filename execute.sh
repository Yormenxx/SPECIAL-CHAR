#!/bin/bash

VENV_NAME=".venv"

echo "--- Starting Char Helper  ---"

if [ ! -d "$VENV_NAME" ]; then
    echo "[!] Entorno virtual no encontrado. Creando uno..."
    python3 -m venv $VENV_NAME

    echo "[!] Instalando dependencias necesarias..."
    ./$VENV_NAME/bin/pip install -r req.txt
fi


echo "[+] Lanzando aplicación..."
./$VENV_NAME/bin/python main.py
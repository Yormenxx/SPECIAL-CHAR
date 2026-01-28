#!/bin/bash

# Definir rutas
APP_DIR="$HOME/.local/share/special-char"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "🚀 Iniciando instalación de SPECIAL-CHAR..."

# 1. Crear carpeta de la aplicación y copiar archivos
mkdir -p "$APP_DIR"
cp -r ./* "$APP_DIR"

# 2. Crear entorno virtual y activar
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate

# 3. Instalar requerimientos (si existen)
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 4. Crear el lanzador .desktop dinámicamente
cat <<EOF > "$DESKTOP_DIR/special-char.desktop"
[Desktop Entry]
Name=Special Char
Comment=Herramienta para gestión de caracteres especiales
Exec=$APP_DIR/venv/bin/python3 $APP_DIR/main.py
Icon=$APP_DIR/icon.png
Terminal=true
Type=Application
Categories=Development;Utility;
EOF

# 5. Dar permisos de ejecución
chmod +x "$DESKTOP_DIR/special-char.desktop"

echo "✅ Instalación completada."
echo "Puedes encontrar la app en tu menú de aplicaciones o ejecutarla desde el escritorio."
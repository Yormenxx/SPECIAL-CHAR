#!/bin/bash

cp -r ./* "$APP_DIR"
APP_DIR="$HOME/.local/share/special-char"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "🚀 Iniciando instalación de SPECIAL-CHAR..."

mkdir -p "$APP_DIR"
cp -r ./* "$APP_DIR"
cd "$APP_DIR"


echo "📦 Configurando entorno virtual y dependencias..."
python3 -m venv venv

./venv/bin/python3 -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    ./venv/bin/pip install -r requirements.txt
else

    ./venv/bin/pip install PyQt6
fi

echo "🖥️  Configurando lanzador como aplicación de escritorio..."
cat <<EOF > "$DESKTOP_DIR/special-char.desktop"
[Desktop Entry]
Name=Special Char
Comment=Herramienta para gestión de caracteres especiales
Exec=$APP_DIR/venv/bin/python3 $APP_DIR/main.py
Icon=$APP_DIR/letraA.jpg
Terminal=false
Type=Application
Categories=Development;Utility;
EOF


chmod +x "$DESKTOP_DIR/special-char.desktop"

echo "✅ ¡Instalación completada con éxito!"
echo "💡 Ya puedes buscar 'Special Char' en tu menú de XFCE."
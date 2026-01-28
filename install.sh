#!/bin/bash

# Definir rutas
APP_DIR="$HOME/.local/share/special-char"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "🚀 Iniciando instalación de SPECIAL-CHAR..."

# 1. Preparar el directorio y copiar archivos
mkdir -p "$APP_DIR"
cp -r ./* "$APP_DIR"
cd "$APP_DIR"

# 2. Configurar el Entorno Virtual (Venv)
echo "📦 Configurando entorno virtual y dependencias..."
python3 -m venv venv
# Usamos la ruta directa al pip del venv para asegurar que se instale ahí
./venv/bin/python3 -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    ./venv/bin/pip install -r requirements.txt
else
    # Si olvidaste el archivo, instalamos PyQt6 por defecto
    ./venv/bin/pip install PyQt6
fi

# 3. Crear el lanzador .desktop
echo "🖥️  Creando acceso directo en el sistema..."
cat <<EOF > "$DESKTOP_DIR/special-char.desktop"
[Desktop Entry]
Name=Special Char
Comment=Herramienta para gestión de caracteres especiales
Exec=bash -c "cd $APP_DIR && $APP_DIR/venv/bin/python3 $APP_DIR/main.py; echo; read -p 'Presiona Enter para cerrar...' -n1 -s"
Icon=$APP_DIR/icon.png
Terminal=true
Type=Application
Categories=Development;Utility;
EOF

# 4. Permisos finales
chmod +x "$DESKTOP_DIR/special-char.desktop"

echo "✅ ¡Instalación completada con éxito!"
echo "💡 Ya puedes buscar 'Special Char' en tu menú de XFCE."
#!/bin/bash
# Crea el acceso directo en el escritorio y lo instala en aplicaciones
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/licitaciones.desktop"
ICON_FILE="$SCRIPT_DIR/icon.png"

# Generate a simple icon if none exists (blue square with "H")
if [ ! -f "$ICON_FILE" ]; then
    python3.12 - <<'PYEOF'
import sys
try:
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (128, 128), color=(0, 48, 135))
    draw = ImageDraw.Draw(img)
    draw.text((44, 36), "H", fill="white")
    img.save("/home/user/licitaciones-project/icon.png")
except ImportError:
    # fallback: create a minimal 1x1 PNG header
    pass
PYEOF
fi

# Update Exec path in .desktop file to use absolute path
sed -i "s|Exec=.*|Exec=/usr/bin/python3.12 $SCRIPT_DIR/launcher.py|g" "$DESKTOP_FILE"
sed -i "s|Icon=.*|Icon=$ICON_FILE|g" "$DESKTOP_FILE"

# Copy to desktop
DESKTOP_DIR="$HOME/Desktop"
mkdir -p "$DESKTOP_DIR"
cp "$DESKTOP_FILE" "$DESKTOP_DIR/licitaciones.desktop"
chmod +x "$DESKTOP_DIR/licitaciones.desktop"

# Also install in applications menu
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"
cp "$DESKTOP_FILE" "$APPS_DIR/licitaciones.desktop"
chmod +x "$APPS_DIR/licitaciones.desktop"

# Update desktop database
update-desktop-database "$APPS_DIR" 2>/dev/null || true

echo ""
echo "✔ Acceso directo instalado en:"
echo "   · Escritorio: $DESKTOP_DIR/licitaciones.desktop"
echo "   · Aplicaciones: $APPS_DIR/licitaciones.desktop"
echo ""
echo "Doble clic en el icono 'Licitaciones Hologic' del escritorio para abrir."

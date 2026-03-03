#!/bin/bash
# ===========================================
# Survey Analytics Dashboard - Start Script
# ===========================================
# Uso: ./start.sh [--port 8000] [--host 0.0.0.0]

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuración por defecto
PORT=8000
HOST=127.0.0.1

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --help)
            echo "Uso: $0 [--port PORT] [--host HOST]"
            echo ""
            echo "Opciones:"
            echo "  --port PORT    Puerto del servidor (default: 8000)"
            echo "  --host HOST    Host del servidor (default: 127.0.0.1)"
            echo "  --help         Mostrar esta ayuda"
            exit 0
            ;;
        *)
            echo -e "${RED}Opción desconocida: $1${NC}"
            exit 1
            ;;
    esac
done

# Cambiar al directorio del backend
cd "$(dirname "$0")/backend"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Survey Analytics Dashboard          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ Entorno virtual no encontrado. Creando...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar dependencias
echo -e "${BLUE}→ Verificando dependencias...${NC}"
pip install -q -r requirements.txt

# Verificar .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ Archivo .env no encontrado${NC}"
    if [ -f ".env.example" ]; then
        echo -e "${BLUE}→ Creando .env desde .env.example${NC}"
        cp .env.example .env
        echo -e "${GREEN}✓ .env creado. Edítalo con tus credenciales.${NC}"
        echo ""
        echo -e "${RED}IMPORTANTE: Debes configurar GROQ_API_KEY y APPS_SCRIPT_URL en el archivo .env${NC}"
        echo ""
        exit 1
    fi
fi

# Iniciar servidor
echo ""
echo -e "${GREEN}→ Iniciando servidor en http://${HOST}:${PORT}${NC}"
echo ""
echo -e "${BLUE}Presiona CTRL+C para detener${NC}"
echo ""

uvicorn main:app --reload --host $HOST --port $PORT

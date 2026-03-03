# 🔗 Google Apps Script - Integración con Google Sheets

Este script convierte tu Google Sheet en una **API JSON** que el backend consume directamente.

---

## 📋 Instalación Rápida

### 1. Abrir Apps Script
1. Abre tu Google Sheet
2. **Extensiones** → **Apps Script**

### 2. Configurar el Código
1. Borra el contenido de `Code.gs`
2. Pega el código de este directorio
3. **Importante:** Cambia `SHEET_NAME` por el nombre exacto de tu hoja

```javascript
const SHEET_NAME = 'Respuestas de formulario 1'; // ← Tu hoja aquí
```

### 3. Implementar como Web App
1. **Implementar** → **Nueva implementación**
2. Tipo: **Aplicación web**
3. Configuración:
   - Ejecutar como: `Yo`
   - Quién tiene acceso: `Cualquier usuario`
4. **Implementar** → Autoriza → Copia la URL

### 4. Conectar con el Backend
Pega la URL en tu archivo `.env` del backend:

```env
APPS_SCRIPT_URL=https://script.google.com/macros/s/TU_ID/exec
```

---

## 🧪 Probar

Abre la URL en tu navegador. Deberías ver:

```json
{
  "success": true,
  "count": 13,
  "data": [...]
}
```

---

## ⚠️ Solución de Problemas

| Error | Solución |
|-------|----------|
| "Hoja no encontrada" | Verifica que `SHEET_NAME` coincida exactamente |
| "Permission denied" | Autoriza el script la primera vez |
| Devuelve vacío | Confirma que hay datos en la hoja (2+ filas) |
| Error CORS | Usa la URL `/exec`, no `/dev` |

---

## 📝 Notas

- **Límites:** 6 min de ejecución, ~100 solicitudes/min
- **No es en tiempo real:** Los cambios en el Sheet se reflejan en la próxima llamada
- **Actualizaciones:** Cada cambio en el código requiere **Nueva implementación**

---

Para más detalles, ver el [README principal](../README.md).

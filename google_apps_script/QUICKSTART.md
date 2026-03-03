# 🚀 Guía Rápida - Conectar Google Sheets con Apps Script

## Resumen

Tienes **dos formas** de conectar tu Google Sheet al dashboard:

| Método | URL | Ventajas |
|--------|-----|----------|
| **CSV Export** | `https://docs.google.com/spreadsheets/d/ID/export?format=csv` | Rápido, sin configuración |
| **Apps Script** | `https://script.google.com/macros/s/XXXXX/exec` | JSON estructurado, más control, recomendado |

---

## 📋 Método Recomendado: Apps Script

### Paso 1: Copia el ID de tu Google Sheet

Tu URL se ve así:
```
https://docs.google.com/spreadsheets/d/1ABC123xyz/edit#gid=0
                                              ↑
                                    Este es el ID
```

### Paso 2: Abre Apps Script

1. En tu Google Sheet: **Extensiones** → **Apps Script**
2. Borra el código predeterminado
3. Pega el contenido de `google_apps_script/Code.gs`

### Paso 3: Configura el Nombre de la Hoja

En `Code.gs`, busca esta línea:
```javascript
const SHEET_NAME = 'Respuestas de formulario 1';
```

Cambia el valor por el nombre **exacto** de tu pestaña (la que tiene los datos).

### Paso 4: Implementa

1. Clic en **Implementar** → **Nueva implementación**
2. Tipo: **Aplicación web**
3. Configuración:
   - **Ejecutar como:** `Yo (tu email)`
   - **Quién tiene acceso:** `Cualquier usuario` (o `Cualquier usuario con cuenta de Google`)
4. Clic en **Implementar**
5. **Autoriza** el script con tu cuenta de Google
6. Copia la URL que termina en `/exec`

### Paso 5: Conecta en el Dashboard

1. Abre tu dashboard: `http://localhost:8000`
2. En la sidebar, pega la URL en el campo **Apps Script**
3. Clic en el botón verde → ¡Listo!

---

## 🔍 Verificar que Funciona

Abre la URL del Web App en tu navegador:
```
https://script.google.com/macros/s/XXXXX/exec
```

Deberías ver algo como:
```json
{
  "success": true,
  "count": 9,
  "data": [
    {
      "id": 1,
      "timestamp": "02/03/2026 22:27:43",
      "attends_in_person": "Sí",
      "open_to_virtual": "No",
      ...
    }
  ]
}
```

---

## 🛠️ Solución de Problemas

### "Hoja no encontrada"
- Verifica que el `SHEET_NAME` en `Code.gs` coincida **exactamente** con tu pestaña
- Los nombres son **sensibles** a mayúsculas/minúsculas

### "Permission denied"
- Asegúrate de haber **autorizado** el script la primera vez
- El Sheet debe ser accesible desde tu cuenta de Google

### "Error CORS"
- Usa la URL que termina en `/exec`, **no** la de `/dev`
- El script ya incluye headers CORS, no necesitas agregar nada

### Los datos no se actualizan
- El Web App lee los datos **en tiempo de ejecución**
- Si agregas filas nuevas, la próxima llamada las incluirá automáticamente

---

## 📊 Estructura de Tus Datos

Tu tabla tiene estas columnas:

| Columna Original | Key en Backend | Tipo |
|-----------------|----------------|------|
| Marca temporal | `timestamp` | Fecha |
| ¿Actualmente asistes presencialmente sin dificultades? | `attends_in_person` | Sí/No/A veces |
| ¿Estarías dispuesto(a) a que la clase pase a modalidad virtual sincrónica? | `open_to_virtual` | Sí/No/Me es indiferente |
| Si la modalidad fuera virtual, ¿contarías con conexión estable a internet? | `has_internet` | Sí/No/A veces falla |
| ¿Dispones de equipo adecuado para clases virtuales? | `has_equipment` | Sí/No/Parcialmente |
| ¿Qué modalidad consideras más efectiva? | `preferred_modality` | Presencial/Virtual/Híbrida |
| Razones para preferir presencial | `reason_presencial` | Texto abierto |
| Razones para preferir virtual/híbrida | `reason_virtual` | Texto abierto |
| Si la clase cambiara a virtual, tu nivel de compromiso sería | `commitment_level` | Mayor/Igual/Menor |
| Comentarios adicionales | `comments` | Texto abierto |

El Apps Script **normaliza** automáticamente:
- Limpia valores vacíos, "NA", "N/A", "Nose", "."
- Convierte fechas al formato correcto
- Mapea nombres largos a claves cortas

---

## 🎯 ¿Cuál Usar?

| Caso | Método |
|------|--------|
| Prototipo rápido | CSV Export |
| Producción | **Apps Script** ✅ |
| Datos sensibles | Apps Script (con acceso restringido) |
| Muchas solicitudes/hora | Apps Script (mejor quota) |

---

**¡Listo, Eddy!** Con Apps Script tienes una integración **profesional, escalable y en tiempo real** con tu Google Sheet.

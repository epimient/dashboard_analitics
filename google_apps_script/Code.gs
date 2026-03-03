/**
 * Google Apps Script - Web App para servir datos de la encuesta
 * Versión: 3.1 - Sin setHeader (no soportado por ContentService)
 * 
 * IMPORTANTE: Después de pegar este código:
 * 1. Guardar (Ctrl+S)
 * 2. Implementar → NUEVA implementación (no editar existente)
 * 3. Tipo: Aplicación web
 * 4. Quién tiene acceso: Cualquier usuario ← ESTO habilita CORS automáticamente
 */

// ------------------------------------------------------------------
// CONFIGURACIÓN - CAMBIA ESTO
// ------------------------------------------------------------------

// Poné el nombre EXACTO de tu pestaña (mirá abajo a la izquierda en tu Sheet)
// Dejalo vacío '' para usar la primera hoja
const SHEET_NAME = '';

// ------------------------------------------------------------------
// CÓDIGO PRINCIPAL
// ------------------------------------------------------------------

function doGet(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet;
    
    if (SHEET_NAME && SHEET_NAME.trim() !== '') {
      sheet = ss.getSheetByName(SHEET_NAME);
      if (!sheet) {
        const names = ss.getSheets().map(s => s.getName()).join(', ');
        throw new Error('Hoja "' + SHEET_NAME + '" no encontrada. Disponibles: ' + names);
      }
    } else {
      sheet = ss.getSheets()[0];
    }
    
    const rows = sheet.getDataRange().getValues();
    
    if (rows.length < 2) {
      return createJSONResponse({
        success: true,
        count: 0,
        data: [],
        message: 'La hoja está vacía o solo tiene encabezados'
      });
    }
    
    const headers = rows[0];
    const data = [];
    
    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];
      const record = { id: i };
      
      for (let j = 0; j < headers.length; j++) {
        const header = headers[j];
        const key = normalizeHeader(header);
        record[key] = cleanValue(row[j], key);
      }
      
      data.push(record);
    }
    
    return createJSONResponse({
      success: true,
      count: data.length,
      data: data
    });
    
  } catch (error) {
    Logger.log('ERROR: ' + error.toString());
    return createJSONResponse({
      success: false,
      error: error.toString(),
      message: 'Error al obtener datos del Google Sheet'
    }, 500);
  }
}

// ------------------------------------------------------------------
// FUNCIONES AUXILIARES
// ------------------------------------------------------------------

function normalizeHeader(header) {
  if (!header || header.toString().trim() === '') {
    return 'unknown';
  }
  
  return header
    .toString()
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')  // Quitar acentos
    .replace(/[^a-z0-9]+/g, '_')       // Reemplazar no alfanuméricos con _
    .replace(/^_|_$/g, '');            // Quitar _ inicial/final
}

function cleanValue(value, key) {
  if (value === null || value === undefined || value === '') {
    return null;
  }
  
  if (value instanceof Date) {
    return Utilities.formatDate(value, Session.getScriptTimeZone(), 'dd/MM/yyyy HH:mm:ss');
  }
  
  if (typeof value === 'number') {
    return value;
  }
  
  const str = value.toString().trim().toLowerCase();
  const placeholders = ['na', 'n/a', 'nose', '.', '-', 'none', 'null'];
  
  if (placeholders.includes(str)) {
    return null;
  }
  
  return value.toString().trim();
}

function createJSONResponse(data, statusCode) {
  const json = JSON.stringify(data);
  
  // ContentService NO soporta setHeader() - CORS se maneja en la implementación
  const output = ContentService.createTextOutput(json);
  output.setMimeType(ContentService.MimeType.JSON);
  
  return output;
}

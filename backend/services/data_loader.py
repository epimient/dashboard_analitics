"""
services/data_loader.py — Clase DataLoader (MVC: Model layer helper).
Carga y normaliza datos de CSV o URL pública de Google Sheets.
"""
from __future__ import annotations
import io
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

import pandas as pd
import numpy as np
import httpx

from config import COLUMN_MAP
from models.survey import SurveyResponse

logger = logging.getLogger(__name__)


class DataLoader:
    """Responsable de leer y normalizar los datos de la encuesta."""

    # Formatos de fecha que may aparecer en Google Sheets
    _DATE_FORMATS = [
        "%d/%m/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    ]

    def load_from_path(self, path: str | Path) -> list[SurveyResponse]:
        """Carga CSV desde el sistema de archivos."""
        csv_path = Path(path)
        if not csv_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        return self._process_dataframe(df)

    def load_from_bytes(self, content: bytes, filename: str = "upload.csv") -> list[SurveyResponse]:
        """Carga CSV desde bytes (upload HTTP)."""
        df = pd.read_csv(io.BytesIO(content), encoding="utf-8-sig")
        return self._process_dataframe(df)

    async def load_from_sheets_url(self, url: str) -> list[SurveyResponse]:
        """
        Carga datos desde una URL pública de Google Sheets.
        La URL debe ser del formulario:
        https://docs.google.com/spreadsheets/d/ID/export?format=csv
        """
        export_url = self._to_csv_export_url(url)
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            resp = await client.get(export_url)
            resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text), encoding="utf-8-sig")
        return self._process_dataframe(df)

    async def load_from_apps_script(self, web_app_url: str) -> list[SurveyResponse]:
        """
        Carga datos desde un Google Apps Script Web App.
        La URL debe ser del formulario:
        https://script.google.com/macros/s/XXXXX/exec

        El Web App debe devolver JSON con esta estructura:
        { "success": true, "count": N, "data": [...] }
        """
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            resp = await client.get(web_app_url)
            resp.raise_for_status()
            data = resp.json()

        if not data.get("success"):
            raise RuntimeError(f"Error del Web App: {data.get('error', 'Desconocido')}")

        df = pd.DataFrame(data.get("data", []))
        return self._process_dataframe(df)

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------

    def _process_dataframe(self, df: pd.DataFrame) -> list[SurveyResponse]:
        """Renombra columnas, limpia valores y construye objetos del dominio."""
        logger.info(f"Procesando DataFrame con {len(df)} filas y columnas: {list(df.columns)}")

        # Renombrar columnas que coincidan con el mapa
        rename: dict[str, str] = {}
        for col in df.columns:
            col_clean = col.strip()
            if col_clean in COLUMN_MAP:
                rename[col] = COLUMN_MAP[col_clean]
                logger.info(f"Mapeando columna: {col} -> {COLUMN_MAP[col_clean]}")
            else:
                logger.warning(f"Columna sin mapeo: {col}")
        df = df.rename(columns=rename)

        # Rellenar NaN con None usando replace de pandas
        df = df.replace({np.nan: None, "nan": None, "NaN": None, "N/A": None, "NA": None})

        responses: list[SurveyResponse] = []
        for idx, row in df.iterrows():
            data = row.to_dict()
            data["id"] = int(idx) + 1
            data["timestamp"] = self._parse_timestamp(data.get("timestamp"))
            # Limpiar strings vacíos y placeholders
            for key, val in data.items():
                if isinstance(val, str):
                    stripped = val.strip()
                    data[key] = None if stripped in ("", "NA", "N/A", "Nose", ".", "-") else stripped
                elif val is None or (hasattr(val, "__class__") and val.__class__.__name__ == "float" and str(val) == "nan"):
                    data[key] = None

            try:
                responses.append(SurveyResponse(**data))
                logger.info(f"Fila {idx + 1} procesada correctamente")
            except Exception as exc:
                logger.warning(f"Fila {idx + 1} ignorada: {exc}")
                logger.debug(f"Datos de fila {idx + 1}: {data}")

        logger.info(f"Total de respuestas procesadas: {len(responses)} de {len(df)} filas")
        return responses

    def _parse_timestamp(self, value: Optional[str]) -> Optional[datetime]:
        if not value:
            return None
        for fmt in self._DATE_FORMATS:
            try:
                return datetime.strptime(str(value).strip(), fmt)
            except ValueError:
                continue
        return None

    @staticmethod
    def _to_csv_export_url(url: str) -> str:
        """Convierte cualquier URL de Google Sheets a su URL de export CSV."""
        if "/export?format=csv" in url:
            return url
        if "spreadsheets/d/" in url:
            sheet_id = url.split("spreadsheets/d/")[1].split("/")[0]
            return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        return url

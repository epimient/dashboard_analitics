"""
models/survey.py — Modelos Pydantic del dominio de encuesta.
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class SurveyResponse(BaseModel):
    """Representa una fila de la encuesta normalizada."""
    id: int
    timestamp: Optional[datetime] = None
    attends_in_person: Optional[str] = None
    open_to_virtual: Optional[str] = None
    has_internet: Optional[str] = None
    has_equipment: Optional[str] = None
    preferred_modality: Optional[str] = None
    reason_presencial: Optional[str] = None
    reason_virtual: Optional[str] = None
    commitment_level: Optional[str] = None
    comments: Optional[str] = None

    model_config = {"from_attributes": True}


class DistributionItem(BaseModel):
    label: str
    count: int
    percentage: float


class SurveyStats(BaseModel):
    """KPIs y distribuciones agregadas."""
    total_responses: int
    # Asistencia presencial
    attends_in_person_dist: list[DistributionItem] = Field(default_factory=list)
    # Disposición a virtual
    open_to_virtual_dist: list[DistributionItem] = Field(default_factory=list)
    # Conexión a internet
    has_internet_dist: list[DistributionItem] = Field(default_factory=list)
    # Equipamiento
    has_equipment_dist: list[DistributionItem] = Field(default_factory=list)
    # Modalidad preferida
    preferred_modality_dist: list[DistributionItem] = Field(default_factory=list)
    # Nivel de compromiso
    commitment_level_dist: list[DistributionItem] = Field(default_factory=list)
    # KPIs calculados
    pct_presencial: float = 0.0
    pct_virtual: float = 0.0
    pct_hibrida: float = 0.0
    pct_stable_internet: float = 0.0
    pct_attends_ok: float = 0.0


class FilterParams(BaseModel):
    """Parámetros opcionales de filtrado."""
    preferred_modality: Optional[str] = None
    open_to_virtual: Optional[str] = None
    has_internet: Optional[str] = None
    has_equipment: Optional[str] = None
    commitment_level: Optional[str] = None

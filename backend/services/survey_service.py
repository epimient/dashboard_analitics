"""
services/survey_service.py — SurveyService (MVC: Model/Service layer).
Lógica de negocio para estadísticas y filtros.
"""
from __future__ import annotations
from collections import Counter
from typing import Optional

from models.survey import SurveyResponse, SurveyStats, DistributionItem, FilterParams


class SurveyService:
    """Proporciona estadísticas y filtrado sobre las respuestas de la encuesta."""

    def __init__(self) -> None:
        self._responses: list[SurveyResponse] = []

    # ------------------------------------------------------------------
    # Estado
    # ------------------------------------------------------------------

    def load(self, responses: list[SurveyResponse]) -> None:
        """Carga (o recarga) el dataset completo en memoria."""
        self._responses = responses

    @property
    def is_loaded(self) -> bool:
        return len(self._responses) > 0

    # ------------------------------------------------------------------
    # Consultas públicas
    # ------------------------------------------------------------------

    def get_all(self, filters: Optional[FilterParams] = None) -> list[SurveyResponse]:
        """Devuelve respuestas aplicando filtros opcionales."""
        data = self._responses
        if filters:
            data = self._apply_filters(data, filters)
        return data

    def get_stats(self, filters: Optional[FilterParams] = None) -> SurveyStats:
        """Calcula KPIs y distribuciones para el dataset filtrado."""
        data = self.get_all(filters)
        total = len(data)

        def distribution(field: str) -> list[DistributionItem]:
            values = [getattr(r, field) for r in data if getattr(r, field)]
            counter = Counter(values)
            return [
                DistributionItem(
                    label=label,
                    count=count,
                    percentage=round(count / total * 100, 2) if total else 0.0,
                )
                for label, count in counter.most_common()
            ]

        def pct(field: str, *matches: str) -> float:
            m = [r for r in data if getattr(r, field) and
                 any(v.lower() in getattr(r, field, "").lower() for v in matches)]
            return round(len(m) / total * 100, 2) if total else 0.0

        return SurveyStats(
            total_responses=total,
            attends_in_person_dist=distribution("attends_in_person"),
            open_to_virtual_dist=distribution("open_to_virtual"),
            has_internet_dist=distribution("has_internet"),
            has_equipment_dist=distribution("has_equipment"),
            preferred_modality_dist=distribution("preferred_modality"),
            commitment_level_dist=distribution("commitment_level"),
            pct_presencial=pct("preferred_modality", "presencial"),
            pct_virtual=pct("preferred_modality", "virtual", "virutal"),
            pct_hibrida=pct("preferred_modality", "híbrida", "hibrida"),
            pct_stable_internet=pct("has_internet", "sí", "si"),
            pct_attends_ok=pct("attends_in_person", "sí", "si"),
        )

    def get_open_responses(self, column_key: str) -> list[str]:
        """Devuelve lista de respuestas no nulas de una columna abierta."""
        return [
            getattr(r, column_key)
            for r in self._responses
            if getattr(r, column_key, None)
        ]

    # ------------------------------------------------------------------
    # Filtrado
    # ------------------------------------------------------------------

    def _apply_filters(
        self, data: list[SurveyResponse], filters: FilterParams
    ) -> list[SurveyResponse]:
        if filters.preferred_modality:
            data = [r for r in data if r.preferred_modality and
                    filters.preferred_modality.lower() in r.preferred_modality.lower()]
        if filters.open_to_virtual:
            data = [r for r in data if r.open_to_virtual and
                    filters.open_to_virtual.lower() in r.open_to_virtual.lower()]
        if filters.has_internet:
            data = [r for r in data if r.has_internet and
                    filters.has_internet.lower() in r.has_internet.lower()]
        if filters.has_equipment:
            data = [r for r in data if r.has_equipment and
                    filters.has_equipment.lower() in r.has_equipment.lower()]
        if filters.commitment_level:
            data = [r for r in data if r.commitment_level and
                    filters.commitment_level.lower() in r.commitment_level.lower()]
        return data

"""
config.py — Configuración global del proyecto.
Usa pydantic-settings para leer variables de entorno o un archivo .env
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- IA ---
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.1-8b-instant", alias="GROQ_MODEL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3", alias="OLLAMA_MODEL")
    default_ai_provider: str = Field(default="ollama", alias="DEFAULT_AI_PROVIDER")

    # --- Datos ---
    default_csv_path: str = Field(default="../data/encuesta.csv", alias="DEFAULT_CSV_PATH")
    apps_script_url: str = Field(
        default="https://script.google.com/macros/s/AKfycbzFj7j-QuSDEWENs612qxr6YncaCbyHEKOfzz5ZasKKyz6blCvVfL4Q4kmLFimgS2p3/exec",
        alias="APPS_SCRIPT_URL"
    )

    # --- Servidor ---
    allowed_origins: list[str] = Field(
        default=["http://localhost:5500", "http://127.0.0.1:5500",
                 "http://localhost:3000", "http://localhost:8000",
                 "null"],
        alias="ALLOWED_ORIGINS",
    )


# Mapeo legible de columnas largas → claves cortas
# Incluye tanto los nombres originales del CSV como las versiones normalizadas de Apps Script
COLUMN_MAP: dict[str, str] = {
    # Nombres originales (CSV)
    "Marca temporal": "timestamp",
    "¿Actualmente asistes presencialmente sin dificultades?": "attends_in_person",
    "¿Estarías dispuesto(a) a que la clase pase a modalidad virtual sincrónica (en vivo en el mismo horario)?": "open_to_virtual",
    "Si la modalidad fuera virtual, ¿contarías con conexión estable a internet durante los horarios de clase?": "has_internet",
    "¿Dispones de equipo adecuado para clases virtuales (computador, micrófono, cámara)?": "has_equipment",
    "¿Qué modalidad consideras más efectiva para tu aprendizaje en esta asignatura?": "preferred_modality",
    "En caso de preferir modalidad presencial, ¿cuáles serían las principales razones? (respuesta abierta)": "reason_presencial",
    "En caso de preferir modalidad virtual o híbrida, ¿cuáles serían las principales razones? (respuesta abierta)": "reason_virtual",
    "Si la clase cambiara a virtual, tu nivel de compromiso sería:": "commitment_level",
    "Comentarios adicionales": "comments",
    # Nombres normalizados (Apps Script - snake_case)
    "marca_temporal": "timestamp",
    "actualmente_asistes_presencialmente_sin_dificultades": "attends_in_person",
    "estarias_dispuesto_a_a_que_la_clase_pase_a_modalidad_virtual_sincronica_en_vivo_en_el_mismo_horario": "open_to_virtual",  # Nota: doble 'a' es intencional
    "si_la_modalidad_fuera_virtual_contarias_con_conexion_estable_a_internet_durante_los_horarios_de_clase": "has_internet",
    "dispones_de_equipo_adecuado_para_clases_virtuales_computador_microfono_camara": "has_equipment",
    "que_modalidad_consideras_mas_efectiva_para_tu_aprendizaje_en_esta_asignatura": "preferred_modality",
    "en_caso_de_preferir_modalidad_presencial_cuales_serian_las_principales_razones_respuesta_abierta": "reason_presencial",
    "en_caso_de_preferir_modalidad_virtual_o_hibrida_cuales_serian_las_principales_razones_respuesta_abierta": "reason_virtual",
    "si_la_clase_cambiara_a_virtual_tu_nivel_de_compromiso_seria": "commitment_level",
    "comentarios_adicionales": "comments",
}

# Columnas de preguntas abiertas que se analizan con IA
OPEN_QUESTIONS: dict[str, str] = {
    "reason_presencial": "Razones para preferir modalidad presencial",
    "reason_virtual": "Razones para preferir modalidad virtual o híbrida",
    "comments": "Comentarios adicionales",
}

settings = Settings()

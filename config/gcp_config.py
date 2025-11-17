"""
Configuration module for Google Cloud services
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class GCPConfig(BaseSettings):
    """Google Cloud Platform Configuration"""
    
    # GCP Project settings
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GCP_CREDENTIALS_PATH: str = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS",
        str(Path.home() / "gcp_credentials.json")
    )
    
    # BigQuery settings
    BIGQUERY_DATASET: str = os.getenv("BIGQUERY_DATASET", "government_schemes")
    BIGQUERY_TABLE: str = os.getenv("BIGQUERY_TABLE", "scheme_data")
    
    # Speech-to-Text settings
    SPEECH_LANGUAGE_CODE: str = os.getenv("SPEECH_LANGUAGE_CODE", "en-US")
    SPEECH_ENCODING: str = "LINEAR16"
    SAMPLE_RATE_HERTZ: int = 16000
    AUDIO_CHUNK_SIZE: int = int(16000 / 10)  # 100ms chunks
    
    # Text-to-Speech settings
    TTS_LANGUAGE_CODE: str = os.getenv("TTS_LANGUAGE_CODE", "en-US")
    TTS_VOICE_NAME: str = os.getenv("TTS_VOICE_NAME", "en-US-Neural2-C")
    TTS_AUDIO_ENCODING: str = "MP3"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


gcp_config = GCPConfig()

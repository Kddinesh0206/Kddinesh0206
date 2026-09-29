from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    app_name: str = "ComicCraft"
    app_env: str = "development"
    debug: bool = True

    # Gemini
    gemini_api_key: str | None = None

    gemini_outline_model: str = "gemini-2.5-flash"
    gemini_story_model: str = "gemini-2.5-pro"

    # Hugging Face
    hf_token: str | None = None

    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"

    # Demo mode
    demo_mode: bool = False

    # Storage
    panels_dir: str = "static/panels"
    exports_dir: str = "static/exports"

    max_prompt_length: int = 2000

    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / "tests" / ".env",
            BASE_DIR / ".env",
        ),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def panels_path(self) -> Path:
        path = BASE_DIR / self.panels_dir
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def exports_path(self) -> Path:
        path = BASE_DIR / self.exports_dir
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache
def get_settings() -> Settings:
    return Settings()
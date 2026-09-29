from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):

    story_prompt: str = Field(
        ...,
        min_length=3,
        max_length=2000
    )

    character_name: str = Field(
        ...,
        min_length=1,
        max_length=80
    )

    setting: str = Field(
        ...,
        min_length=1,
        max_length=120
    )

    tone: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    art_style: str = Field(
        ...,
        min_length=1,
        max_length=80
    )

    @field_validator("*")
    @classmethod
    def clean_values(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty.")

        return value


class ImageTestRequest(BaseModel):

    prompt: str = Field(
        ...,
        min_length=3,
        max_length=2000
    )


class PanelOutline(BaseModel):

    panel_number: int = Field(
        ...,
        ge=1,
        le=5
    )

    title: str

    scene_description: str

    image_prompt: str


class OutlineResponse(BaseModel):

    panels: list[PanelOutline] = Field(
        ...,
        min_length=5,
        max_length=5
    )


class StoryPanel(BaseModel):

    panel_number: int = Field(
        ...,
        ge=1,
        le=5
    )

    caption: str

    narration: str

    dialogue: str


class StoryResponse(BaseModel):

    panels: list[StoryPanel] = Field(
        ...,
        min_length=5,
        max_length=5
    )


class ComicPanel(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str

    caption: str

    narration: str

    dialogue: str

    image_url: str


class ComicResponse(BaseModel):

    panels: list[ComicPanel]

    pdf_url: str

    filename: str
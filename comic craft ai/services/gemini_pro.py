from google import genai
from google.genai import types

from app.config import Settings
from app.models import OutlineResponse, StoryResponse


def create_client(settings: Settings):

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_story(
    outline: list[dict],
    character_name: str,
    tone: str,
    settings: Settings
) -> list[dict]:

    if settings.demo_mode:

        dialogue = [
            f"Let's see where this leads, {tone.lower()}ly!",
            "Oh no, that wasn't part of the plan.",
            "Wait, I know just what to do.",
            "Here goes nothing!",
            "We did it together!",
        ]

        panels = [
            {
                "panel_number": panel["panel_number"],
                "caption": panel["title"],
                "narration": panel["scene_description"],
                "dialogue": dialogue[panel["panel_number"] - 1],
            }
            for panel in outline
        ]

        return [
            panel.model_dump()
            for panel in StoryResponse(panels=panels).panels
        ]

    client = create_client(settings)

    validated_outline = OutlineResponse(
        panels=outline
    )

    prompt = f"""
You are a professional comic-book writer.

Expand this five-panel outline into polished comic writing.

MAIN CHARACTER:
{character_name}

TONE:
{tone}

OUTLINE:
{validated_outline.model_dump_json(indent=2)}

For every panel generate:

1. caption
   A short comic-style environmental or dramatic caption.

2. narration
   A concise description of the character's action,
   emotion and story progression.

3. dialogue
   Natural character dialogue.
   If dialogue is unnecessary, return an empty string.

IMPORTANT:

- Return exactly five panels.
- Preserve the panel numbers.
- Preserve story continuity.
- Do not change the main character.
- Do not create additional panels.
- Keep the writing suitable for a comic book.
"""

    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StoryResponse,
            temperature=0.85,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty story."
        )

    parsed = StoryResponse.model_validate_json(
        response.text
    )

    return [
        panel.model_dump()
        for panel in parsed.panels
    ]
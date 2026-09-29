from google import genai
from google.genai import types

from app.config import Settings
from app.models import OutlineResponse


def create_client(settings: Settings):

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
    settings: Settings
) -> list[dict]:

    if settings.demo_mode:

        beats = [
            ("A Curious Beginning", f"takes the first step toward {story_prompt}"),
            ("An Unexpected Challenge", "meets a surprising obstacle"),
            ("A Clever Idea", "finds a thoughtful way forward"),
            ("A Brave Attempt", "puts the new plan into action"),
            ("A Bright Ending", "celebrates a warm and satisfying resolution"),
        ]

        outline = [
            {
                "panel_number": panel_number,
                "title": title,
                "scene_description": (
                    f"{character_name} {action} in {setting}."
                ),
                "image_prompt": (
                    f"{art_style} comic illustration: {character_name} "
                    f"{action} in {setting}. Inspired by {story_prompt}."
                ),
            }
            for panel_number, (title, action) in enumerate(
                beats,
                start=1
            )
        ]

        return [
            panel.model_dump()
            for panel in OutlineResponse(panels=outline).panels
        ]

    client = create_client(settings)

    prompt = f"""
You are a professional comic story planner.

Create a coherent five-panel comic outline.

USER STORY:
{story_prompt}

MAIN CHARACTER:
{character_name}

SETTING:
{setting}

TONE:
{tone}

ART STYLE:
{art_style}

IMPORTANT REQUIREMENTS:

1. Generate exactly 5 panels.
2. Every panel must move the story forward.
3. Keep the same main character throughout.
4. Maintain visual continuity.
5. Give every panel a clear title.
6. Give every panel a scene description.
7. Give every panel a detailed image-generation prompt.
8. Do not include dialogue inside image_prompt.
9. Do not include text, letters, captions, speech bubbles,
   logos or watermarks inside image_prompt.
10. Make the story have a clear beginning, middle and ending.
"""

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=OutlineResponse,
            temperature=0.9,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty outline."
        )

    parsed = OutlineResponse.model_validate_json(
        response.text
    )

    return [
        panel.model_dump()
        for panel in parsed.panels
    ]
from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageDraw
from huggingface_hub import InferenceClient

from app.config import Settings
from utils.files import safe_filename


def create_demo_image(
    prompt: str,
    output: Path
):

    width = 1024
    height = 1024

    image = Image.new(
        "RGB",
        (width, height),
        "#f5ead8"
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (25, 25, width - 25, height - 25),
        outline="#222222",
        width=8
    )

    draw.text(
        (70, 70),
        "COMICCRAFT",
        fill="#222222"
    )

    draw.text(
        (70, 130),
        "DEMO PANEL",
        fill="#222222"
    )

    words = prompt.split()

    lines = []

    current_line = ""

    for word in words[:60]:

        if len(current_line) + len(word) > 55:

            lines.append(current_line)

            current_line = word

        else:

            current_line += " " + word

    if current_line:
        lines.append(current_line)

    y = 230

    for line in lines[:12]:

        draw.text(
            (70, y),
            line,
            fill="#333333"
        )

        y += 45

    image.save(
        output,
        format="PNG"
    )


def generate_image(
    prompt: str,
    panel_number: int,
    settings: Settings
) -> Path:

    filename = (
        f"panel-{panel_number}-"
        f"{safe_filename(str(uuid4()))}.png"
    )

    output = (
        settings.panels_path /
        filename
    )

    # Allows testing without API keys.
    if settings.demo_mode:

        create_demo_image(
            prompt,
            output
        )

        return output

    if not settings.hf_token:

        raise RuntimeError(
            "HF_TOKEN is not configured."
        )

    client = InferenceClient(
        provider="auto",
        api_key=settings.hf_token
    )

    final_prompt = f"""
{prompt}

Create a high-quality comic-book illustration.

Visual requirements:

- cinematic composition
- professional comic illustration
- expressive character
- consistent character appearance
- detailed environment
- strong lighting
- clean line art
- rich colors
- professional graphic novel quality

Do NOT include:
- text
- letters
- speech bubbles
- captions
- logos
- watermarks
"""

    image = client.text_to_image(
        final_prompt,
        model=settings.hf_image_model
    )

    image.save(
        output,
        format="PNG"
    )

    return output
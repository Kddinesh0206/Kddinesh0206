from app.config import Settings

from services.gemini_flash import (
    generate_outline
)

from services.gemini_pro import (
    generate_story
)

from services.image_generator import (
    generate_image
)

from services.layout_builder import (
    build_comic_layout
)

from services.exporters import (
    save_pdf
)

from utils.files import (
    public_static_path
)


def generate_comic(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
    settings: Settings
) -> dict:

    # --------------------------------
    # STEP 1
    # Generate 5-panel outline
    # --------------------------------

    outline = generate_outline(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style,
        settings=settings
    )

    # --------------------------------
    # STEP 2
    # Generate narration/dialogue
    # --------------------------------

    story = generate_story(
        outline=outline,
        character_name=character_name,
        tone=tone,
        settings=settings
    )

    # --------------------------------
    # STEP 3
    # Generate images
    # --------------------------------

    image_paths = []

    for panel in outline:

        image_path = generate_image(
            prompt=panel["image_prompt"],
            panel_number=panel["panel_number"],
            settings=settings
        )

        image_paths.append(
            image_path
        )

    # --------------------------------
    # STEP 4
    # Convert image paths to URLs
    # --------------------------------

    static_root = (
        settings.panels_path.parent
    )

    image_urls = [

        public_static_path(
            path,
            static_root
        )

        for path in image_paths
    ]

    # --------------------------------
    # STEP 5
    # Build comic layout
    # --------------------------------

    layout = build_comic_layout(
        outline=outline,
        story=story,
        image_urls=image_urls
    )

    # --------------------------------
    # STEP 6
    # Prepare PDF data
    # --------------------------------

    pdf_layout = []

    for panel, image_path in zip(
        layout,
        image_paths
    ):

        item = dict(panel)

        item["image_path"] = str(
            image_path
        )

        pdf_layout.append(
            item
        )

    # --------------------------------
    # STEP 7
    # Generate PDF
    # --------------------------------

    pdf_path = save_pdf(
        layout=pdf_layout,
        exports_dir=settings.exports_path
    )

    # --------------------------------
    # STEP 8
    # Return result
    # --------------------------------

    pdf_url = public_static_path(
        pdf_path,
        settings.exports_path.parent
    )

    return {

        "layout": layout,

        "pdf_url": pdf_url,

        "filename": pdf_path.name
    }
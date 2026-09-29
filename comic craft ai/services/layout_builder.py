def build_comic_layout(
    outline: list[dict],
    story: list[dict],
    image_urls: list[str]
) -> list[dict]:

    story_by_panel = {
        item["panel_number"]: item
        for item in story
    }

    layout = []

    for panel in outline:

        number = panel["panel_number"]

        story_item = story_by_panel.get(
            number
        )

        if not story_item:

            raise ValueError(
                f"Missing story data for panel {number}."
            )

        layout.append({

            "panel_number": number,

            "title": panel["title"],

            "scene_description":
                panel["scene_description"],

            "image_prompt":
                panel["image_prompt"],

            "caption":
                story_item["caption"],

            "narration":
                story_item["narration"],

            "dialogue":
                story_item["dialogue"],

            "image_url":
                image_urls[number - 1]
        })

    return layout
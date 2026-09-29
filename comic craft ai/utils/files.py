import re
from pathlib import Path


def safe_filename(
    value: str,
    max_length: int = 50
) -> str:

    value = value.strip().lower()

    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value
    )

    value = re.sub(
        r"-+",
        "-",
        value
    ).strip("-")

    return value[:max_length] or "comic"


def public_static_path(
    path: Path,
    static_root: Path
) -> str:

    relative = path.relative_to(static_root)

    return "/static/" + relative.as_posix()
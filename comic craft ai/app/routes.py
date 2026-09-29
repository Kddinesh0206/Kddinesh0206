from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import HTMLResponse

from fastapi.templating import (
    Jinja2Templates
)

from app.config import (
    get_settings
)

from app.models import (
    PromptRequest,
    ImageTestRequest
)

from services.comic_generator import (
    generate_comic
)

from services.image_generator import (
    generate_image
)

from utils.files import (
    public_static_path
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    settings = get_settings()

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={

            "request": request,

            "demo_mode":
                settings.demo_mode
        }
    )


@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(

    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)
):

    settings = get_settings()

    try:

        story_prompt = story_prompt.strip()

        if len(story_prompt) > settings.max_prompt_length:

            raise ValueError(
                f"Story prompt cannot exceed "
                f"{settings.max_prompt_length} characters."
            )

        result = generate_comic(

            story_prompt=story_prompt,

            character_name=character_name,

            setting=setting,

            tone=tone,

            art_style=art_style,

            settings=settings
        )

        return templates.TemplateResponse(

            request=request,

            name="comic_preview.html",

            context={

                "request": request,

                "layout":
                    result["layout"],

                "pdf_url":
                    result["pdf_url"],

                "filename":
                    result["filename"]
            }
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={

                "request": request,

                "error": str(exc)
            },

            status_code=500
        )


@router.get(
    "/generate",
    response_class=HTMLResponse
)
async def generate_form(
    request: Request
):

    settings = get_settings()

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={

            "request": request,

            "demo_mode":
                settings.demo_mode
        }
    )


@router.post(
    "/generate-comic/json"
)
async def generate_comic_json(
    payload: PromptRequest
):

    settings = get_settings()

    try:

        result = generate_comic(

            story_prompt=
                payload.story_prompt,

            character_name=
                payload.character_name,

            setting=
                payload.setting,

            tone=
                payload.tone,

            art_style=
                payload.art_style,

            settings=settings
        )

        return result

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)

        ) from exc


@router.post(
    "/test-image"
)
async def test_image(
    payload: ImageTestRequest
):

    settings = get_settings()

    try:

        path = generate_image(

            prompt=payload.prompt,

            panel_number=1,

            settings=settings
        )

        static_root = (
            settings.panels_path.parent
        )

        return {

            "image_url":
                public_static_path(
                    path,
                    static_root
                )
        }

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)

        ) from exc


@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(

    request: Request,

    filename: str = "comic"
):

    return templates.TemplateResponse(

        request=request,

        name="export_success.html",

        context={

            "request": request,

            "filename": filename
        }
    )


@router.get("/health")
async def health():

    settings = get_settings()

    return {

        "status": "ok",

        "app":
            settings.app_name,

        "demo_mode":
            settings.demo_mode,

        "gemini_configured":
            bool(
                settings.gemini_api_key
            ),

        "huggingface_configured":
            bool(
                settings.hf_token
            )
    }
from datetime import datetime
from pathlib import Path

from fpdf import FPDF


class ComicPDF(FPDF):

    def header(self):

        self.set_font(
            "Helvetica",
            "B",
            16
        )

        self.cell(
            0,
            10,
            "ComicCraft",
            ln=True,
            align="C"
        )

        self.ln(3)


def save_pdf(
    layout: list[dict],
    exports_dir: Path
) -> Path:

    exports_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        "comiccraft-"
        f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
    )

    output = exports_dir / filename

    pdf = ComicPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            15
        )

        pdf.set_x(pdf.l_margin)

        pdf.multi_cell(
            0,
            9,
            f"Panel {panel['panel_number']}: "
            f"{panel['title']}"
        )

        pdf.ln(3)

        image_path = Path(
            panel["image_path"]
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=15,
                y=None,
                w=180
            )

            pdf.ln(5)

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )

        pdf.set_x(pdf.l_margin)

        pdf.multi_cell(
            0,
            6,
            panel["scene_description"]
        )

        pdf.ln(3)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.set_x(pdf.l_margin)

        pdf.multi_cell(
            0,
            7,
            "Caption"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.set_x(pdf.l_margin)

        pdf.multi_cell(
            0,
            7,
            panel["caption"]
        )

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.set_x(pdf.l_margin)

        pdf.multi_cell(
            0,
            7,
            "Narration"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.set_x(pdf.l_margin)

        pdf.multi_cell(
            0,
            7,
            panel["narration"]
        )

        if panel["dialogue"]:

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.set_x(pdf.l_margin)

            pdf.multi_cell(
                0,
                7,
                "Dialogue"
            )

            pdf.set_font(
                "Helvetica",
                "",
                11
            )

            pdf.set_x(pdf.l_margin)

            pdf.multi_cell(
                0,
                7,
                panel["dialogue"]
            )

    pdf.output(
        str(output)
    )

    return output
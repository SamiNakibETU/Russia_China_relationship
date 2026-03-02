"""
Generate PDF report from analysis results.

Output: reports/Russia_China_Dependency_Report.pdf
Usage: python scripts/generate_pdf_report.py
"""
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORTS = PROJECT_ROOT / "reports"
FIGURES = REPORTS / "figures"
OUT_PDF = REPORTS / "Russia_China_Dependency_Report.pdf"


def main() -> None:
    doc = SimpleDocTemplate(str(OUT_PDF), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=22, textColor="#1a1a1a")
    story.append(Paragraph("Russia-China dependency", title_style))
    story.append(Paragraph("Quantitative analysis 2017-2024", styles["Heading2"]))
    story.append(Spacer(1, 0.25 * inch))

    story.append(Paragraph("Executive summary", styles["Heading1"]))
    summary = (
        "HHI 0.40 (extreme concentration). Russia 67.5% exports to China, asymmetry 7.2x. "
        "Event study post-2022: +53.6% trade (p<0.001). Russia migrated from European to Asian trade bloc. "
        "MDI dual-use share 2.67-7.98%, Carnegie ~300 M$/mo."
    )
    story.append(Paragraph(summary, styles["BodyText"]))
    story.append(Spacer(1, 0.2 * inch))

    data = [
        ["Metric", "Value"],
        ["HHI", "0.40"],
        ["Event study post-2022", "+53.6%"],
        ["MDI range", "2.67-7.98%"],
        ["Break cost (baseline)", "8 mo"],
    ]
    story.append(Table(data))
    story.append(PageBreak())

    story.append(Paragraph("Figures", styles["Heading1"]))
    figures = [
        (FIGURES / "mdi_timeline.png", "MDI evolution 2022-2024"),
        (FIGURES / "hhi_timeline.png", "HHI concentration"),
        (FIGURES / "crink_network_graph.png", "CRINK trade network"),
    ]
    for path, caption in figures:
        if path.exists():
            story.append(Image(str(path), width=6 * inch, height=4 * inch))
            story.append(Paragraph(caption, styles["Normal"]))
            story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
    print(f"PDF generated: {OUT_PDF}")


if __name__ == "__main__":
    main()

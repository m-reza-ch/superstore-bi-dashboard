from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(kpis):
    doc = SimpleDocTemplate("superstore_report.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    flow = [Paragraph("<b>Superstore Analytics Report</b>", styles["Title"])]

    for k, v in kpis.items():
        flow.append(Paragraph(f"{k}: {v}", styles["BodyText"]))

    doc.build(flow)

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table

def generate_pdf(data, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Smart Offer Analysis Report", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Total Income", f"${data['total_income']:,.2f}"],
        ["Federal Tax", f"${data['federal_tax']:,.2f}"],
        ["Retirement Contribution", f"${data['retirement_contribution']:,.2f}"],
        ["Net Income", f"${data['net_income']:,.2f}"],
    ]

    table = Table(table_data)
    elements.append(table)

    doc.build(elements)

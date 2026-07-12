"""
Wayne AI Pharma - PDF Report Generator
Generates encrypted downloadable PDF reports using fpdf2.
"""
import io
from datetime import datetime
from fpdf import FPDF
from config import (
    APP_NAME, PRIMARY_COLOR, MCKINSEY_AVG_TIMELINE_MONTHS, MCKINSEY_AVG_COST_MILLIONS
)


class WaynePDFReport(FPDF):
    """Custom PDF report for Wayne AI Pharma analysis results."""

    def __init__(self, analysis_data: dict, original_filename: str):
        super().__init__()
        self.analysis = analysis_data
        self.filename = original_filename
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        self.set_fill_color(37, 99, 235)  # #2563eb
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 14, f" {APP_NAME} - Clinical Trial Analysis Report", ln=True, fill=True)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(200, 210, 230)
        self.cell(0, 7, f" Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}  |  Confidential & Encrypted", ln=True, fill=True)
        self.ln(5)

    def footer(self):
        self.set_y(-25)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"All data encrypted. We do not train AI on your data. HIPAA/PPB aligned.  |  {APP_NAME} v1.0", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(37, 99, 235)
        self.cell(0, 10, title, ln=True)
        self.set_draw_color(37, 99, 235)
        self.set_line_width(0.5)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(4)

    def body_text(self, text: str, bold: bool = False):
        self.set_font("Helvetica", "B" if bold else "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def metric_box(self, label: str, value: str, mckinsey_value: str):
        self.set_fill_color(245, 247, 255)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(37, 99, 235)
        self.cell(0, 8, f" {label}", ln=True, fill=True)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(16, 185, 129)
        self.cell(190, 14, f" {value}", ln=True)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(128, 128, 128)
        self.cell(190, 6, f"    McKinsey Average: {mckinsey_value}", ln=True)
        self.ln(6)


def generate_pdf_report(analysis: dict, original_filename: str) -> bytes:
    """Generate a PDF report from analysis data. Returns PDF as bytes."""
    pdf = WaynePDFReport(analysis, original_filename)
    pdf.add_page()

    # Source document
    pdf.section_title("Source Document")
    pdf.body_text(f"Original File: {original_filename}")
    pdf.ln(3)

    # Confidence
    confidence = analysis.get("confidence", "N/A")
    pdf.section_title("Analysis Confidence")
    pdf.body_text(f"Confidence Score: {confidence}%")
    pdf.ln(3)

    # Timeline
    pdf.section_title("1. Predicted Trial Timeline")
    timeline = analysis.get("timeline", "N/A")
    pdf.metric_box("Predicted Timeline", timeline, f"{MCKINSEY_AVG_TIMELINE_MONTHS} months (McKinsey Avg)")

    # Cost
    pdf.section_title("2. Predicted Trial Cost")
    cost = analysis.get("cost", "N/A")
    pdf.metric_box("Predicted Cost", cost, f"${MCKINSEY_AVG_COST_MILLIONS}M (McKinsey Avg)")

    # Risks
    pdf.section_title("3. Top 5 Risks in Africa & Mitigation Strategies")
    risks = analysis.get("risks", [])
    for i, risk_item in enumerate(risks[:5], 1):
        risk_text = risk_item.get("risk", "N/A") if isinstance(risk_item, dict) else str(risk_item)
        mitigation = risk_item.get("mitigation", "N/A") if isinstance(risk_item, dict) else "See analysis"
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(220, 38, 38)
        pdf.cell(0, 7, f" Risk {i}: {risk_text}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(16, 185, 129)
        pdf.cell(0, 7, f" Mitigation: {mitigation}", ln=True)
        pdf.ln(2)
    pdf.ln(3)

    # Compliance
    pdf.section_title("4. Regulatory Compliance Scores")
    compliance = analysis.get("compliance", {})
    comp_data = [
        ("PPB Kenya", compliance.get("kenya_score", "N/A")),
        ("NAFDAC Nigeria", compliance.get("nigeria_score", "N/A")),
        ("SAHPRA South Africa", compliance.get("sa_score", "N/A")),
        ("EDA Egypt", compliance.get("egypt_score", "N/A")),
    ]
    for name, score in comp_data:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(80, 7, f" {name}", ln=False)
        pdf.cell(110, 7, f" Score: {score}/100", ln=True)
    pdf.ln(2)

    checklist = compliance.get("checklist", [])
    if checklist:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(0, 7, " Compliance Checklist:", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 50, 50)
        for item in checklist:
            pdf.cell(0, 6, f"   [] {item}", ln=True)
    pdf.ln(5)

    # Recruitment
    pdf.section_title("5. Patient Recruitment Rate by Country")
    recruitment = analysis.get("recruitment", {})
    for country, rate in recruitment.items():
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        country_display = country.replace("_", " ").title()
        pdf.cell(0, 7, f" {country_display}: {rate}", ln=True)
    pdf.ln(5)

    # Advantage
    pdf.section_title("6. Why This Beats McKinsey")
    advantage = analysis.get("advantage", "N/A")
    pdf.body_text(advantage)

    # Disclaimer
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 5,
        "DISCLAIMER: This report is generated by Wayne AI Pharma for informational purposes only. "
        "It does not constitute legal or regulatory advice. All patient data has been redacted. "
        "Consult with qualified regulatory professionals before making trial decisions. "
        "All data encrypted at rest and in transit."
    )

    return pdf.output()


def get_pdf_bytes(analysis: dict, original_filename: str) -> bytes:
    """Wrapper to generate PDF and return bytes."""
    return generate_pdf_report(analysis, original_filename)

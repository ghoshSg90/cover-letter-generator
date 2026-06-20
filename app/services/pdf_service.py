from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(content, output_file):

    doc = SimpleDocTemplate(output_file)

    styles = getSampleStyleSheet()

    story = [
        Paragraph(content, styles["Normal"])
    ]

    doc.build(story)

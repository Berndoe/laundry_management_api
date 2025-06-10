from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string


def generate_pdf(template_path, context):
    """
    Generates a PDF file given an HTML file and context
    :param template_path: the path to the html file
    :param context: the details to be put in the file
    :return: PDF file
    """
    html_content = render_to_string(template_path, context)
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    pdf_file.seek(0)
    return pdf_file if not pisa_status.err else None

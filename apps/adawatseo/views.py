import base64
import io

from PyPDF2 import PdfReader
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .lib.helpers import loop_in_chunks


class ExtractPDFTextView(APIView):
    parser_classes = [MultiPartParser, FileUploadParser]

    def post(self, request: Request, format=None):
        pdf_file = request.data.get("files")

        if not pdf_file:
            return Response({"error": "No PDF file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract text
            with io.BytesIO(pdf_file.read()) as pdf_data:
                reader = PdfReader(pdf_data)
                text = "\n".join([page.extract_text() for page in reader.pages])

            return Response({"text": text})

        except Exception as e:
            print(f"Error processing PDF: {e}")
            return Response(
                {"error": "Failed to process PDF"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TextToPDFView(APIView):

    def post(self, request: Request):
        text = request.data.get("files")

        if not text:
            text = request.data.get("plainText")
            if not text:
                return Response(
                    {"error": "No Text content uploaded"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            text = text.read().decode("utf-8")

        # PDF generation logic
        pdf_buffer = io.BytesIO()
        pdf_document = canvas.Canvas(pdf_buffer)
        textobject = pdf_document.beginText(2 * cm, 29.7 * cm - 2 * cm)
        for line in text.splitlines(False):
            if len(line) > 80:
                for chunk in loop_in_chunks(line):
                    textobject.textLine(chunk.rstrip())
            else:
                textobject.textLine(line.rstrip())

        pdf_document.drawText(textobject)

        pdf_document.save()
        pdf_data = pdf_buffer.getvalue()
        pdf_buffer.close()

        return Response({"pdf_data": base64.b64encode(pdf_data)}, content_type="application/pdf")

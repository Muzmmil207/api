import io

from PyPDF2 import PdfReader
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ExtractPDFTextView(APIView):
    parser_classes = [MultiPartParser, FileUploadParser]

    def post(self, request: Request, format=None):
        pdf_file = request.data.get("files")
        print(request.data)
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

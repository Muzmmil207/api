import base64
import io
import os
import shutil
import subprocess
from io import BytesIO

import PIL
import webp
from django.conf import settings
from PIL import Image
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class IcoToPngConverter(APIView):
    def post(self, request, format=None):
        try:
            # Get ICO data from request (replace 'ico_data' with actual field name)
            ico_data = request.FILES.get("ico")
            if not ico_data:
                return Response({"error": "Invalid ICO file"})

            # Read ICO data using icoreader
            reader = "icoreader".Reader(ico_data)
            # Assuming you want the first icon in the ICO file
            first_icon = reader.read(0)  # Adjust index for specific icon

            # Convert ICO image to PNG format
            png_image = first_icon.as_  # PIL.Image()  # Assuming using Pillow for PNG conversion

            # Prepare response with converted PNG data (base64 encoding)
            response_data = {"png_data": base64.b64encode(png_image.getvalue()).decode("utf-8")}
            return Response(response_data)
        except Exception as e:
            print(f"Error converting ICO: {e}")
            return Response(
                {"error": "There was an error converting the ICO file."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class JpgToPngConverter(APIView):
    def post(self, request, format=None):
        try:
            # Get JPG data from request (replace 'jpg_data' with actual field name)
            jpg_data = request.FILES.get("jpg_data")
            if not jpg_data or not jpg_data.content_type.startswith("image/jpeg"):
                return Response({"error": "Invalid JPG file"})

            # Open the JPG image using Pillow
            image = Image.open(jpg_data)

            # Convert to PNG format
            response_data = {
                "png_data": base64.b64encode(image.convert("RGB").getvalue()).decode("utf-8")
            }
            return Response(response_data)
        except Exception as e:
            print(f"Error converting JPG: {e}")
            return Response(
                {"error": "There was an error converting the JPG file."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class WebPToJpgConverter(APIView):
    def post(self, request, format=None):
        try:
            # Get WebP data from request (replace 'webp_data' with actual field name)
            webp_data = request.FILES.get("webp_data")
            if not webp_data or not webp_data.content_type.startswith("image/webp"):
                return Response({"error": "Invalid WebP file"})

            # Read WebP data into a BytesIO object
            webp_buffer = BytesIO(webp_data.read())

            # Decode WebP image using webp or pillow-webp library
            webp_image = webp.load_image(webp_buffer)  # Adjust based on your chosen library

            # Prepare a BytesIO object for the output JPG image
            jpg_buffer = BytesIO()

            # Encode the WebP image as JPG with desired quality (optional)
            jpg_image = webp_image.convert("RGB")  # Ensure compatible color mode
            jpg_image.save(jpg_buffer, format="JPEG", quality=80)  # Adjust quality as needed

            # Prepare response with converted JPG data (base64 encoding)
            response_data = {"jpg_data": base64.b64encode(jpg_buffer.getvalue()).decode("utf-8")}
            return Response(response_data)
        except Exception as e:
            print(f"Error converting WebP: {e}")
            return Response(
                {"error": "There was an error converting the WebP file."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PngToWebPConverter(APIView):
    def post(self, request, format=None):
        try:
            # Get PNG data from request (replace 'png_data' with actual field name)
            png_data = request.FILES.get("png_data")
            if not png_data or not png_data.content_type.startswith("image/png"):
                return Response({"error": "Invalid PNG file"})

            # Read PNG data into a BytesIO object
            png_buffer = BytesIO(png_data.read())

            # Decode PNG image using Pillow (assuming installed)
            from PIL import Image

            png_image = Image.open(png_buffer)

            # Prepare a BytesIO object for the output WebP image
            webp_buffer = BytesIO()

            # Encode the PNG image as WebP with desired quality (optional)
            webp_image = png_image.convert("RGB")  # Ensure compatible color mode
            webp.encode(webp_image, webp_buffer, quality=80)  # Adjust quality as needed

            # Prepare response with converted WebP data (base64 encoding)
            response_data = {"webp_data": base64.b64encode(webp_buffer.getvalue()).decode("utf-8")}
            return Response(response_data)
        except Exception as e:
            print(f"Error converting PNG: {e}")
            return Response(
                {"error": "There was an error converting the PNG file."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PNGToBMPView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        png_file = request.FILES.get("image")
        if not png_file or not png_file.name.lower().endswith(".png"):
            return Response({"error": "Only PNG files are supported"}, status=400)

        try:
            # Open PNG image using Pillow
            image = PIL.Image.open(png_file)

            # BMP format typically doesn't support transparency (alpha channel)
            # Convert to RGB mode if the image has a transparency channel
            if image.mode in ("RGBA", "LA"):
                image = image.convert("RGB")

            # Create a byte buffer to store the BMP data
            output_buffer = io.BytesIO()

            # Save as BMP
            image.save(output_buffer, format="BMP")

            # Get BMP data
            bmp_data = output_buffer.getvalue()

            return Response({"bmp": bmp_data}, content_type="image/bmp")

        except Exception as e:
            return Response({"error": f"Conversion failed: {e}"}, status=500)


class PNGToGIFView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        png_file = request.FILES.get("image")
        if not png_file or not png_file.name.lower().endswith(".png"):
            return Response({"error": "Only PNG files are supported"}, status=400)

        try:
            # Read PNG image
            image = PIL.Image.open(png_file)

            # Convert to RGB mode if not already
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Create a byte buffer for the GIF output
            output_buffer = io.BytesIO()

            # Configure GIF parameters (adjust as needed)
            fps = 10  # Adjust frames per second
            transparency = 0  # Adjust transparency (0-255)

            # Save as GIF
            image.save(
                output_buffer,
                format="GIF",
                append_images=[image],
                save_all=True,
                fps=fps,
                transparency=transparency,
            )

            # Get GIF data
            gif_data = output_buffer.getvalue()

            return Response({"gif": gif_data}, content_type="image/gif")

        except Exception as e:
            return Response({"error": f"Conversion failed: {e}"}, status=500)


class PNGToICOView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        png_file = request.FILES.get("image")
        if not png_file or not png_file.name.lower().endswith(".png"):
            return Response({"error": "Only PNG files are supported"}, status=400)

        try:
            # Check if imagemagick is installed (adjust for your OS)
            if not shutil.which("convert"):  # Assuming convert command from imagemagick
                return Response(
                    {"error": "ImageMagick (convert) is required for conversion"}, status=400
                )

            # Generate a unique filename for the temporary ICO file
            filename, extension = os.path.splitext(png_file.name)
            ico_filename = f"{filename}.ico"
            ico_path = os.path.join(
                settings.MEDIA_ROOT, ico_filename
            )  # Adjust path based on your settings

            # Save uploaded PNG
            with open(ico_path, "wb") as destination:
                for chunk in png_file.chunks():
                    destination.write(chunk)

            # Convert PNG to ICO using imagemagick (adjust command if needed)
            subprocess.run(["convert", ico_path, ico_path], check=True)

            # Read the converted ICO data
            with open(ico_path, "rb") as ico_file:
                ico_data = ico_file.read()

            # Delete temporary ICO file
            os.remove(ico_path)

            return Response({"ico": ico_data}, content_type="image/vnd.microsoft.icon")

        except Exception as e:
            return Response({"error": f"Conversion failed: {e}"}, status=500)


class JPGToWebpView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        jpg_file = request.FILES.get("image")
        if not jpg_file or not jpg_file.name.lower().endswith((".jpg", ".jpeg")):
            return Response({"error": "Only JPG/JPEG files are supported"}, status=400)

        try:
            # Open JPG image using Pillow
            image = PIL.Image.open(jpg_file)

            # Convert the image to RGB mode for WEBP saving (if not already)
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Create a byte buffer to store the WEBP data
            output_buffer = io.BytesIO()

            # Configure WEBP parameters (adjust as needed)
            quality = 80  # Adjust quality (0-100)

            # Save as WEBP
            image.save(output_buffer, format="WEBP", quality=quality)

            # Get WEBP data
            webp_data = output_buffer.getvalue()

            return Response({"webp": webp_data}, content_type="image/webp")

        except Exception as e:
            return Response({"error": f"Conversion failed: {e}"}, status=500)


class JPGToBMPView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        jpg_file = request.FILES.get("image")
        if not jpg_file or not jpg_file.name.lower().endswith((".jpg", ".jpeg")):
            return Response({"error": "Only JPG/JPEG files are supported"}, status=400)

        try:
            # Open JPG image using Pillow
            image = PIL.Image.open(jpg_file)

            # BMP format generally doesn't support transparency or alpha channel
            # Convert to RGB mode if the image has transparency channel
            if image.mode in ("RGBA", "LA"):
                image = image.convert("RGB")

            # Create a byte buffer to store the BMP data
            output_buffer = io.BytesIO()

            # Save as BMP
            image.save(output_buffer, format="BMP")

            # Get BMP data
            bmp_data = output_buffer.getvalue()

            return Response({"bmp": bmp_data}, content_type="image/bmp")

        except Exception as e:
            return Response({"error": f"Conversion failed: {e}"}, status=500)


class JPGToGIFView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        jpg_file = request.FILES.get("image")
        if not jpg_file or not jpg_file.name.lower().endswith(".jpg"):
            return Response({"error": "Only JPG files are supported"}, status=400)

        try:
            # Open JPG image using Pillow
            image = PIL.Image.open(jpg_file)

            # JPG doesn't support animation, so create a simple GIF with a single frame
            frames = [image.convert("RGB")]  # Ensure RGB mode for GIF

            # Create a byte buffer to store the GIF data
            output_buffer = io.BytesIO()

            # Configure GIF parameters (adjust as needed)
            fps = 1  # Adjust frames per second (since it's a single frame, FPS won't affect much)
            transparency = 0  # Adjust transparency (0-255)

            # Save as GIF
            frames[0].save(
                output_buffer,
                format="GIF",
                append_images=frames,
                save_all=True,
                fps=fps,
                transparency=transparency,
            )

            # Get GIF data
            gif_data = output_buffer.getvalue()

            return Response({"gif": gif_data}, content_type="image/gif")

        except Exception as e:
            return Response({"error": f"Conversion failed: {e}"}, status=500)


class JPGToICOView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        jpg_file = request.FILES.get("image")
        if not jpg_file or not jpg_file.name.lower().endswith(".jpg"):
            return Response({"error": "Only JPG files are supported"}, status=400)

        try:
            # Check if imagemagick is installed (adjust for your OS)
            if not shutil.which("convert"):  # Assuming convert command from imagemagick
                return Response(
                    {"error": "ImageMagick (convert) is required for conversion"}, status=400
                )

            # Generate a unique filename for the temporary JPG and ICO files
            filename, extension = os.path.splitext(jpg_file.name)
            jpg_filename = f"{filename}.jpg"
            ico_filename = f"{filename}.ico"
            jpg_path = os.path.join(
                settings.MEDIA_ROOT, jpg_filename
            )  # Adjust path based on your settings
            ico_path = os.path.join(settings.MEDIA_ROOT, ico_filename)

            # Save uploaded JPG
            with open(jpg_path, "wb") as destination:
                for chunk in jpg_file.chunks():
                    destination.write(chunk)

            # Resize JPG to various sizes commonly used in ICO files (adjust as needed)
            resize_commands = [
                f"convert {jpg_path} -resize 16x16 {jpg_path[:-4]}_16x16.jpg",
                f"convert {jpg_path} -resize 24x24 {jpg_path[:-4]}_24x24.jpg",
                f"convert {jpg_path} -resize 32x32 {jpg_path[:-4]}_32x32.jpg",
                f"convert {jpg_path} -resize 48x48 {jpg_path[:-4]}_48x48.jpg",
            ]
            for command in resize_commands:
                subprocess.run(command.split(), check=True)

            # Create ICO file using imagemagick (adjust command if needed)
            subprocess.run(
                ["convert", "-delay", "0", f"{jpg_path[:-4]}*.jpg", ico_path], check=True
            )

            # Read the converted ICO data
            with open(ico_path, "rb") as ico_file:
                ico_data = ico_file.read()

            # Delete temporary files
            for filename in [jpg_filename, ico_filename] + [
                f
                for f in os.listdir(settings.MEDIA_ROOT)
                if f.endswith(".jpg") and f.startswith(filename)
            ]:
                os.remove(os.path.join(settings.MEDIA_ROOT, filename))

            return Response({"ico": ico_data}, content_type="image/vnd.microsoft.icon")

        except Exception as e:
            return Response({"error": f"Conversion failed: {e}"}, status=500)


class WEBPToPNGView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        webp_file = request.FILES.get("image")
        if not webp_file or not webp_file.name.lower().endswith(".webp"):
            return Response({"error": "Only WEBP files are supported"}, status=400)

        try:
            # Open WEBP image using Pillow
            image = PIL.Image.open(webp_file)

            # WEBP can be transparent, so ensure mode is RGBA for PNG conversion
            if image.mode != "RGBA":
                image = image.convert("RGBA")

            # Create a byte buffer to store the PNG data
            output_buffer = io.BytesIO()

            # Save as PNG
            image.save(output_buffer, format="PNG")

            # Get PNG data
            png_data = output_buffer.getvalue()

            return Response({"png": png_data}, content_type="image/png")

        except Exception as e:
            return Response({"error": f"Conversion failed: {e}"}, status=500)

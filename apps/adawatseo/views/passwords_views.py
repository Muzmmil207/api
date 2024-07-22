import base64
import binascii
import hashlib

from django.contrib.auth.password_validation import validate_password
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class PasswordValidator(APIView):
    def post(self, request:Request):
        try:
            # Get WebP data from request (replace 'webp_data' with actual field name)
            password = request.data.get("password")
            if not password:
                return Response({"error": "Password is required!"})
            validate_password(password)
            return Response({'content':'Strong'})
        except Exception as e:
            return Response(
                {"error": "<br>".join(e)},
            )





def encrypt_password(password, algorithm):
   

    if algorithm == 'DES':
        # DES is not secure for password storage. Use a stronger algorithm!
        # This example would require the pyDes library (pip install pyDes).
        # from des import DES, CBC
        # key = b'your_secret_key'  # Replace with a strong key
        # iv = b'\0\0\0\0\0\0\0\0'  # Replace with a random initialization vector
        # cipher = DES(key, CBC, iv, pad=None, padmode=PAD_PKCS7)
        # encrypted_password = cipher.encrypt(password.encode())
        # return base64.b64encode(encrypted_password).decode()
        raise ValueError("DES is not recommended for password storage.")

    elif algorithm == 'md5':
        # MD5 is not secure for password storage. Use a stronger algorithm!
        hasher = hashlib.md5()
        hasher.update(password.encode())
        return hasher.hexdigest()

    elif algorithm == 'sha1':
        # SHA1 is not secure for password storage. Use a stronger algorithm!
        hasher = hashlib.sha1()
        hasher.update(password.encode())
        return hasher.hexdigest()

    elif algorithm == 'uuEncode':
        return binascii.uuencode(password.encode()).decode()

    elif algorithm == 'base64':
        return base64.b64encode(password.encode()).decode()

    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

from rest_framework.response import Response
from rest_framework.views import APIView


class PasswordEncryptionView(APIView):
    def post(self, request):
        password = request.data.get('password')
        algorithm = request.data.get('algorithm')

        if not password or not algorithm:
            return Response({'error': 'Missing required fields: password or algorithm'}, status=400)

        try:
            encrypted_password = encrypt_password(password, algorithm)
            return Response({'encrypted_password': encrypted_password})
        except ValueError as e:
            return Response({'error': str(e)}, status=400)





            
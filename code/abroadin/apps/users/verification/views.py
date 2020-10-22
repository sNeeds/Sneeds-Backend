from verification.views import BaseGenerateVerificationAPIView, BaseVerifyVerificationAPIView

from .utils import send_email_verification


class GenerateVerificationAPIView(BaseGenerateVerificationAPIView):
    send_code_function = send_email_verification


class VerifyVerificationAPIView(BaseVerifyVerificationAPIView):
    pass

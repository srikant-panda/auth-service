import secrets


class OTPService:
    def __init__(self):
        self.otp = secrets.randbelow(900000) + 100000
        

    def generate_otp(self):
        if self.otp:
            return self.otp
        self.generate_otp()
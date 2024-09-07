import random
import string


def generate_otp(length: int = 6) -> str:
    otp = ""
    for _ in range(length):
        otp += str(random.choice(string.digits))
    return otp

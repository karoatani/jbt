import datetime
import pyotp


def generate(number: int = 30):
    """
    Generate otp codes

    :param number: Time(in seconds) of when otp expires
    """
    otp = pyotp.totp.TOTP(pyotp.random_base32())

    otp.interval = number
    return otp

from firebase_admin import auth


def send_otp(phone_number):
    verification = auth.create_custom_token(phone_number)
    return verification


def verify_otp(verification_id, code):
    try:
        auth.verify_id_token(verification_id, code)
        return True
    except auth.AuthError:
        return False

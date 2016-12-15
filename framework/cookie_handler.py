from hashlib import sha256

#random string
SECRET = "ruhdb9msrDMKETQUfoW7Ak0Ik94aXViC9A7GCpn7X5qEI0ULKm9QkrTNZG2Ql4yGlG1bCINShafzKpsKmNF5GQ=="


def sign_cookie(value):
    string_value = str(value)
    signature = sha256(SECRET + string_value).hexdigest()
    return signature + "|" + string_value

    # browser declare the cookie


def check_cookie(value):
    signature = value[:value.find('|')]
    declared_value = value[value.find('|') + 1:]

    if sha256(SECRET + declared_value).hexdigest() == signature:
        return declared_value
    else:
        return None

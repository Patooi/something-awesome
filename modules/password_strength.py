import pwnedpasswords
import re
import secrets
import string


def check_breaches(password):
    breaches = pwnedpasswords.check(password)
    return breaches


def is_valid_master(password):
    min_length = 14

    num_breaches = pwnedpasswords.check(password)

    if len(password) < min_length:
        return (False, "Password must be greater than 12 characters.")
    elif num_breaches != 0:
        return (False, f"Password has appeared in {num_breaches} breaches")
    elif not re.search(r"[A-Z]", password):
        return (False, "Password must have at least one upper-case letter.")
    elif not re.search(r"[a-z]", password):
        return (False, "Password must have at least one lower-case letter.")
    elif not re.search(r"[0-9]", password):
        return (False, "Password must have at least one number.")
    elif not re.search(r"[!@#$%^&*()_+\-=\[\]{};:\\|,.<>\/?~\'\"]", password):
        return (False, "Password must have at least one special character")
    elif re.search(r"\s", password):
        return (False, "Password must not contain whitespaces")

    return (True, "Valid Password.")


def generate_password(length, characters):
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password

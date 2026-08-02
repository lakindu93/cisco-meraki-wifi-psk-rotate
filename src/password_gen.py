import secrets
import string


def generate_psk(length: int = 8, special_char_count: int = 2, special_chars: str = "!@#$%^&*-_") -> str:
    if special_char_count > length:
        raise ValueError("special_char_count cannot exceed total length")

    alnum_chars = string.ascii_letters + string.digits
    body_length = length - special_char_count

    chars = []
    if body_length >= 1:
        chars.append(secrets.choice(string.ascii_lowercase))
    if body_length >= 2:
        chars.append(secrets.choice(string.ascii_uppercase))
    if body_length >= 3:
        chars.append(secrets.choice(string.digits))
    chars += [secrets.choice(alnum_chars) for _ in range(body_length - len(chars))]
    chars += [secrets.choice(special_chars) for _ in range(special_char_count)]

    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

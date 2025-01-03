import bcrypt


def get_hashed_password(password: str) -> bytes:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(pw, salt)
    return hashed_password


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

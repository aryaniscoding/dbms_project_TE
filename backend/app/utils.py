from passlib.context import CryptContext
pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256")


def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)

def verify_password(pw: str, pw_hash: str) -> bool:
    return pwd_ctx.verify(pw, pw_hash)

def grade_from_marks(m: int):
    # Returns (letter, points)
    if m >= 90: return ("O", 10.0)
    if m >= 80: return ("A+", 9.0)
    if m >= 70: return ("A", 8.0)
    if m >= 60: return ("B+", 7.0)
    if m >= 50: return ("B", 6.0)
    if m >= 40: return ("C", 5.0)
    return ("F", 0.0)

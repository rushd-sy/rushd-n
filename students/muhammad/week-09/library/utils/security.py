from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

def verify_password(plain_password: str, hashed_password: str = DUMMY_HASH) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(plain_password: str) -> str:
    return password_hash.hash(plain_password)

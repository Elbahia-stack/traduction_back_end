from pwdlib import PasswordHash

# Utilise la configuration recommandée
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    # Correction de 'has' -> 'hash'
    return password_hash.hash(password[:72])  # tronquer pour bcrypt si nécessaire

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Tronquer également lors de la vérification
    return password_hash.verify(plain_password[:72], hashed_password)

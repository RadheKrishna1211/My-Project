import hashlib

def encrypt_password(password):
    """
    Encrypts the provided password using SHA-256 algorithm.
    
    Parameters:
        password (str): The password to be encrypted.
        
    Returns:
        str: The encrypted password.
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

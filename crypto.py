from cryptography.fernet import Fernet
import base64
import hashlib


def gerar_chave(master_password):
    chave = hashlib.sha256(
        master_password.encode()
    ).digest()

    return base64.urlsafe_b64encode(chave)


def criptografar(texto, senha_mestra):
    f = Fernet(gerar_chave(senha_mestra))
    return f.encrypt(texto.encode()).decode()


def descriptografar(token, senha_mestra):
    f = Fernet(gerar_chave(senha_mestra))
    return f.decrypt(token.encode()).decode()

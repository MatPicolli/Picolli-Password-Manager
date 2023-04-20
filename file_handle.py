from cryptography.fernet import Fernet

def encrypt_file():
    # Gera uma chave de criptografia aleatória
    key = Fernet.generate_key()

    # Cria um objeto Fernet com a chave gerada
    fernet = Fernet(key)

    # Le o conteúdo do arquivo CSV a ser criptografado
    with open('senhas.csv', 'rb') as file:
        original = file.read()

    # Criptografa o conteúdo do arquivo CSV
    encrypted = fernet.encrypt(original)

    # Grava o conteúdo criptografado em um arquivo
    with open('senhas.csv', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt_file():

    # Descriptografa o conteúdo do arquivo CSV criptografado
    with open('senhas.csv', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)

    # Grava o conteúdo descriptografado em um arquivo
    with open('senhas.csv', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
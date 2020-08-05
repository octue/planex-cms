import os
from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("-----------\nGenerated key:")
print(key.decode("utf-8"))
os.environ["KOMBU_FERNET_KEY"] = key.decode("utf-8")
print("-----------\nAdd this as a secret to the travis file by using the travis CLI with the following command:")
print(f'travis encrypt --add --pro KOMBU_FERNET_KEY={key.decode("utf-8")}')
print("-----------")

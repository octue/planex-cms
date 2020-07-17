import os
from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("Generated key: ", key.decode("utf-8"))
os.environ["KOMBU_FERNET_KEY"] = key.decode("utf-8")

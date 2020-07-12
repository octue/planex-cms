import os
from cryptography.fernet import Fernet

key = Fernet.generate_key()
os.environ["KOMBU_FERNET_KEY"] = str(key)

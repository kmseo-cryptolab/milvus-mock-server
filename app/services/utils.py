from he_func import generate_key


class AESKeyManager:
    def __init__(self):
        self.aes_key: str


class CKKSKeyManager:
    def __init__(self):
        self.pub_key: str
        self.pri_key: str

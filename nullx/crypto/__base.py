class Crypto:
    pass

class Middleware(Crypto):
    def _self_has_key(self, key):
        try:
            getattr(self, key)
            return True
        except AttributeError:
            return False

    def _set_props(self, allowed_keys, kwargs):
        for key, value in kwargs.items():
            if key in allowed_keys and not self._self_has_key(key):
                setattr(self, key, value)

    def run(self):
        pass

class Cipher(Crypto):
    def encrypt(self):
        pass

    def decrypt(self):
        pass

class CipherCracker(Middleware):
    pass


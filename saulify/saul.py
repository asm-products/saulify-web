import hashlib
import base64
import random


def api_key_gen():
    hash_key = hashlib.sha256(str(random.getrandbits(256))).digest()
    rand_symb = random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])
    return base64.b64encode(hash_key, rand_symb).rstrip('==')

# May it be "clean" function here (from view show_article)

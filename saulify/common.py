import hashlib
import base64
import random
import time
from flask import g, request
from saulify import app
from functools import wraps
from flask.ext.login import current_user

def api_key_gen():
    hash_key = hashlib.sha256(str(random.getrandbits(256))).digest()
    rand_symb = random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])
    return base64.b64encode(hash_key, rand_symb).rstrip('==')

def get_slug_from_int(i):
    alphabet = "01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(alphabet)

    if i == 0:
        return alphabet[0]

    ret = ""
    while i:
        ret = alphabet[i % base] + ret
        i = i // base

    return ret

def get_int_from_slug(s):
    ret, mult = 0, 1
    for ch in reversed(s):
        ret += mult*basedigits.index(ch)
        mult *= BASE
    return ret

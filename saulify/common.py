import hashlib
import base64
import random
import time
from flask import g, request
from saulify import app
from functools import wraps
from flask.ext.login import current_user

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def api_key_gen():
    hash_key = hashlib.sha256(str(random.getrandbits(256))).digest()
    rand_symb = random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])
    return base64.b64encode(hash_key, rand_symb).rstrip('==')


def get_slug_from_int(i):
    base = len(ALPHABET)

    if i == 0:
        return ALPHABET[0]

    ret = ""
    while i:
        ret = ALPHABET[i % base] + ret
        i = i // base

    return ret


def get_int_from_slug(s):
    base = len(ALPHABET)
    ret, mult = 0, 1
    for ch in reversed(s):
        ret += mult*ALPHABET.index(ch)
        mult *= base
    return ret

from datetime import timedelta, datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

token_expire_time = datetime.now() + timedelta(hours=3, minutes=30)

time = datetime.now()


def generate_alphanum_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.sample(letters_and_digits, length))


def hash_password(password: str):
    return generate_password_hash(password=password)


def check_password(hash_pass, password):
    return check_password_hash(pwhash=hash_pass, password=password)

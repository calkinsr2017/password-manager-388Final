from datetime import datetime
import random

def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")


# Random password generator
def random_password():
    str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()?"
    passLen = 12
    password = "".join(random.sample(str,passLen))
    return password
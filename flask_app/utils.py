from datetime import datetime
import random
import re

def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")


# Random password generator
def random_password():
    str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()?"
    passLen = 12
    password = "".join(random.sample(str,passLen))
    return password

# one lowercase, one uppercase, one number one special character, no spaces
def verifyPassword(password):
    if(len(password) < 6 or len(password) > 32):
        return False
    flag = True
    while True:   
        if not re.search("[A-Z]", password): 
            flag = False
            break
        elif not re.search("[0-9]", password):
            flag = False
            break
        elif not re.search("[!@#$%^&*()?]", password): 
            flag = False
            break
        elif re.search("\s", password): 
            flag = False
            break
        break    
    return flag
    
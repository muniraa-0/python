import random
import string

length = 12
characters = string.ascii_letters + string.digits
password = ''.join(random.choice(characters) for _ in range(length))
password_list = list(password)
random.shuffle(password_list)
password = ''.join(password_list)

print("Generated Password:", password)
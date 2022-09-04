import os
import random
import string
os.system("rm -rf auth")
os.system("mkdir auth")
passwords=[]
for x in range(1, 17):
    os.system(f"mkdir auth/team{x}")
    password=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    os.system(f"htpasswd -Bcb ./auth/team{x}/registry.password team{x} {password}")
    passwords.append(password)



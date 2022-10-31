import os
import random
import string
import docker
import time
import json
passwords=[]
if(not os.path.exists("passwords.json")):
    for x in range(1, 13):
        os.system(f"mkdir auth/team{x}")
        password=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        os.system(f"htpasswd -Bcb ./auth/team{x}/registry.password team{x} {password}")
        passwords.append(password)
    json.dump(passwords, open("passwords.json", 'w'))
    exit(0)
else:
    passwords=json.load(open("./passwords.json", "r"))

for x in range(len(passwords)):
    print(f"Team {x+1} password {passwords[x]}")

time.sleep(3)
client=docker.from_env()
for x in range(1, 13):
    print(f"Setting up for team {x}")
    print(f"docker build ../ -f Dockerfile.bot -t team{x}.registry.rising0.com/bot/bot:latest")
    os.system(f"docker login https://team{x}.registry.rising0.com -u team{x} -p {passwords[x-1]}")
    os.system(f"docker push team{x}.registry.rising0.com/bot/bot:latest")

client.images.build(path="../", dockerfile="Dockerfile", tag=f"kothbackend:latest")




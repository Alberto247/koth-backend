import os
import random
import string
import docker
import time
import json

os.system("rm auth/*/*")
os.system("mkdir auth")
passwords=[]
for x in range(1, 17):
    os.system(f"mkdir auth/team{x}")
    password=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    os.system(f"htpasswd -Bcb ./auth/team{x}/registry.password team{x} {password}")
    passwords.append(password)

for x in range(len(passwords)):
    print(f"Team {x+1} password {passwords[x]}")

time.sleep(3)
client=docker.from_env()
for x in range(1, 17):
    print(f"Setting up for team {x}")
    print(client.images.build(path="../", dockerfile="Dockerfile.bot", tag=f"team{x}.registry.alberto247.xyz:7394/bot/bot:latest"))
    os.system(f"docker login https://team{x}.registry.alberto247.xyz:7394 -u team{x} -p {passwords[x-1]}")
    os.system(f"docker push team{x}.registry.alberto247.xyz:7394/bot/bot:latest")

client.images.build(path="../", dockerfile="Dockerfile", tag=f"kothbackend:latest")


json.dump(passwords, open("passwords.json", 'w'))

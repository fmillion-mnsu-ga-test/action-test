# CS 480 Deployment Script
# by Flint Million (11-28-2023)

# This deploys a CS 480 Quiz 2 project on the server.
# It must be run as part of a GitHub action!

# Dependencies
#   - 
import os
import os.path
import shutil
import subprocess
import sys

print("Now deploying your CS 480 project...")

SRC_PATH = os.environ["GITHUB_WORKSPACE"]
if not os.path.isfile(os.path.join(SRC_PATH,"docker-compose.yml")):
    print("ERROR: You don't have a Docker Compose file in your repository!")
    exit(1)

GH_USER = os.environ["GITHUB_ACTOR"]
print(f"Your GitHub user: {GH_USER}")

# Make directory for the user if it does not exist
DOCKER_PATH=f"/managed/{GH_USER}"
os.makedirs(DOCKER_PATH,exist_ok=True)

# switch to the new directory
os.chdir(DOCKER_PATH)

# If a docker-compose file already exists, take down the stack
if os.path.isfile(os.path.join(DOCKER_PATH,"docker-compose.yml")):
    print("Shutting down existing Docker stack.")
    subprocess.run(["docker","compose","down"],stderr=subprocess.STDOUT)

# Copy the entire repository to this directory
print("Copying your project to the Docker service directory.")
retcode = subprocess.call(["rsync","-art","--delete",SRC_PATH+"/",DOCKER_PATH+"/"],stderr=subprocess.STDOUT)
if retcode:
    print("ERROR: Something went wrong copying files. Check with the developer - it may not be your fault.")
    exit(1)

# Start up the stack!
print("Starting up your Docker stack.")
retcode = subprocess.call(["docker","compose","up","-d","--remove-orphans"],stderr=subprocess.STDOUT)
if retcode:
    print("ERROR: Something went wrong starting your stack. Check syntax and re-check the instructions and try again!")
    exit(1)
print("Finished!")

print("Deployment task completed successfully! If all went well you should be able to access your site as per the instructions.")
exit(0)
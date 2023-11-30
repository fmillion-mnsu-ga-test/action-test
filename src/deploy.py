import os
import os.path
import shutil
import subprocess
import sys

print("Now deploying your CS 480 project...")

if len(sys.argv) < 2:
    print("ERROR: script invocation error, please contact developer.")
    exit(1)

SRC_PATH = sys.argv[1]
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
    os.system("docker compose down")
    print("Finished!")

# Copy the entire repository to this directory
subprocess.run(["rsync","--delete",SRC_PATH+"/",DOCKER_PATH+"/"])
print("Copied project to Docker service directory.")

# Start up the stack!
print("Starting up the new Docker stack...")
os.system("docker compose up -d --remove-orphans")
print("Finished!")

print("Deployment task completed successfully!")

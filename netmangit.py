import os
import requests
import shutil

# Set the GitHub repository URL
repo_url = "https://github.com/prathz111/NetmanLab5"

# Set the access token
access_token = "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"

# Set the local directory to clone the repository
local_dir = "/home/netman/Documents/Lab5Midterm/Lab5_python"

# Create a directory if it doesn't exist
if not os.path.exists(local_dir):
    os.makedirs(local_dir)
    print("Created directory:", local_dir)

# Clone the GitHub repository if it doesn't exist locally
if not os.path.exists(os.path.join(local_dir, ".git")):
    os.chdir(local_dir)
    os.system("git init")
    os.system("git remote add origin {}".format(repo_url))
    os.system("git fetch")
    os.system("git checkout {}".format("main"))
    print("Cloned repository:", repo_url)

# Add the .txt and .jpg files to the staging area
os.chdir(local_dir)
os.system("touch file.txt")
os.system("touch file.jpg")
os.system("git add .")
print("Added files to staging area")

# Commit the changes to the local repository
os.system('git commit -m "Added files"')
print("Committed changes to local repository")

# Push the changes to the GitHub repository
os.system("git push origin {}".format("main"))
print("Pushed changes to remote repository")

# Get the latest changes from the GitHub repository
response = requests.get("https://api.github.com/repos/prathz111/NetmanLab5/commits?per_page=1&access_token=" + access_token)
sha = response.json()[0]["sha"]
url = "https://github.com/prathz111/NetmanLab5/archive/{}.zip".format(sha)
response = requests.get(url, stream=True)
with open("repo.zip", "wb") as f:
    shutil.copyfileobj(response.raw, f)
print("Downloaded latest changes from GitHub repository")

# Extract the downloaded repository zip file
shutil.unpack_archive("repo.zip", local_dir)
print("Extracted downloaded zip file to:", local_dir)

# Check for differences between the local and remote repositories
os.chdir(local_dir)
diff = os.system("git diff origin/main")
if diff != 0:
    print("There are differences between local and remote repositories")
else:
    print("No differences between local and remote repositories")

# Add the modified files to the staging area
os.system("git add .")
print("Added modified files to staging area")

# Commit the changes to the local repository
os.system('git commit -m "Modified files"')
print("Committed changes to local repository")

# Push the changes to the GitHub repository
os.system("git push origin {}".format("main"))
print("Pushed changes to remote repository")

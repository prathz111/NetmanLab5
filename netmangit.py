import os
import requests

# Set the GitHub repository URL
repo_url = "https://api.github.com/repos/prathz111/NetmanLab5"

# Set the access token
access_token = "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"

# Create the headers for the API request
headers = {"Authorization": "Bearer " + access_token, "Accept": "application/vnd.github.v3+json"}

# Get the latest commit SHA for the default branch
response = requests.get(repo_url + "/commits", headers=headers)
response.raise_for_status()
sha = response.json()[0]["sha"]
print("hhhh")
# Set the local directory name
local_dir = "/home/netman/Documents/Lab5Midterm/Lab5_python"

# Clone the GitHub repository if it doesn't exist locally
if not os.path.exists(local_dir):
    os.system("git clone " + repo_url + ".git " + local_dir)

# Change directory to the local directory
os.chdir(local_dir)

# Add the .txt and .jpg files to the staging area
os.system("git add file.txt file.jpg")

# Commit the changes to the local repository
os.system("git commit -m 'Added files'")

# Push the changes to the GitHub repository
os.system("git push " + repo_url + " HEAD:master")

# Get the latest changes from the GitHub repository
os.system("git pull " + repo_url)

# Compare the modified files in the local repository against the GitHub repository
os.system("git diff " + sha)

# Add the modified files to the staging area
os.system("git add .")

# Commit the changes to the local repository
os.system("git commit -m 'Modified files'")

# Push the changes to the GitHub repository
os.system("git push " + repo_url + " HEAD:master")

# Print that the push was successful
print("Pushed changes to remote repository.")
